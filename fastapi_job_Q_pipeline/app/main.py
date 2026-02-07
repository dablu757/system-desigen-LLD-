from __future__ import annotations

import io
import json
import uuid
from typing import Optional

from fastapi import FastAPI, File, Form, HTTPException, UploadFile
from fastapi.responses import FileResponse
from rq import Queue

from app.database import get_redis
from app.models import JobCreateResponse, JobStatusResponse, PipelineConfig
from app.settings import settings
from app.tasks import run_pipeline_job
from infrastructure.file_storage import FileStorage
from infrastructure.repository import JobRepository

app = FastAPI(title="Excel Pipeline API")


@app.get("/health")
def health() -> dict:
    return {"status": "ok"}


@app.post("/upload", response_model=JobCreateResponse)
async def upload_excel(
    file: UploadFile = File(...),
    config: Optional[str] = Form(default=None),
    callback_url: Optional[str] = Form(default=None),
) -> JobCreateResponse:
    if not file.filename:
        raise HTTPException(status_code=400, detail="Missing filename")

    pipeline_config = None
    if config:
        try:
            pipeline_config = PipelineConfig(**json.loads(config)).model_dump()
        except Exception as exc:  # noqa: BLE001
            raise HTTPException(status_code=400, detail=f"Invalid config: {exc}") from exc

    storage = FileStorage(settings.storage_dir)
    content = await file.read()
    input_path = storage.save_upload(file.filename, io.BytesIO(content))

    job_id = uuid.uuid4().hex
    redis_client = get_redis()
    repo = JobRepository(redis_client)
    repo.create_job(
        job_id,
        {
            "input_path": input_path,
            "pipeline_config": pipeline_config,
            "callback_url": callback_url,
        },
    )

    queue = Queue(settings.queue_name, connection=redis_client)
    queue.enqueue(run_pipeline_job, job_id)

    return JobCreateResponse(job_id=job_id, status="QUEUED")


@app.get("/jobs/{job_id}", response_model=JobStatusResponse)
def get_job(job_id: str) -> JobStatusResponse:
    redis_client = get_redis()
    repo = JobRepository(redis_client)
    job = repo.get_job(job_id)
    if not job:
        raise HTTPException(status_code=404, detail="Job not found")
    return JobStatusResponse(
        job_id=job_id,
        status=job.get("status", "UNKNOWN"),
        created_at=job.get("created_at"),
        updated_at=job.get("updated_at"),
        error=job.get("error"),
        result=job.get("result"),
    )


@app.get("/jobs/{job_id}/result")
def download_result(job_id: str):
    redis_client = get_redis()
    repo = JobRepository(redis_client)
    job = repo.get_job(job_id)
    if not job:
        raise HTTPException(status_code=404, detail="Job not found")

    if job.get("status") != "COMPLETED":
        raise HTTPException(status_code=400, detail="Job not completed")

    result = job.get("result") or {}
    output_path = result.get("output_path")
    if not output_path:
        raise HTTPException(status_code=404, detail="Output not found")

    return FileResponse(output_path, filename="output.csv")
