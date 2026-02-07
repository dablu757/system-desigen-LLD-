from __future__ import annotations

import json
from typing import Optional

from fastapi import Depends, FastAPI, File, Form, HTTPException, UploadFile
from fastapi.responses import FileResponse

from app.dependencies import get_query_service, get_submission_service
from app.models import JobCreateResponse, JobStatusResponse, PipelineConfig
from app.services import (
    JobNotCompletedError,
    JobNotFoundError,
    JobOutputMissingError,
    JobQueryService,
    JobSubmissionService,
)

app = FastAPI(title="Excel Pipeline API")


@app.get("/health")
def health() -> dict:
    return {"status": "ok"}


@app.post("/upload", response_model=JobCreateResponse)
async def upload_excel(
    file: UploadFile = File(...),
    config: Optional[str] = Form(default=None),
    callback_url: Optional[str] = Form(default=None),
    submission_service: JobSubmissionService = Depends(get_submission_service),
) -> JobCreateResponse:
    if not file.filename:
        raise HTTPException(status_code=400, detail="Missing filename")

    pipeline_config = None
    if config:
        try:
            pipeline_config = PipelineConfig(**json.loads(config)).model_dump()
        except Exception as exc:  # noqa: BLE001
            raise HTTPException(status_code=400, detail=f"Invalid config: {exc}") from exc

    file_content = await file.read()
    job_id = submission_service.submit(
        filename=file.filename,
        file_content=file_content,
        pipeline_config=pipeline_config,
        callback_url=callback_url,
    )
    return JobCreateResponse(job_id=job_id, status="QUEUED")


@app.get("/jobs/{job_id}", response_model=JobStatusResponse)
def get_job(
    job_id: str,
    query_service: JobQueryService = Depends(get_query_service),
) -> JobStatusResponse:
    try:
        job = query_service.get_job(job_id)
    except JobNotFoundError as exc:
        raise HTTPException(status_code=404, detail="Job not found") from exc

    return JobStatusResponse(
        job_id=job_id,
        status=job.get("status", "UNKNOWN"),
        created_at=job.get("created_at"),
        updated_at=job.get("updated_at"),
        error=job.get("error"),
        result=job.get("result"),
    )


@app.get("/jobs/{job_id}/result")
def download_result(
    job_id: str,
    query_service: JobQueryService = Depends(get_query_service),
):
    try:
        output_path = query_service.get_result_path(job_id)
    except JobNotFoundError as exc:
        raise HTTPException(status_code=404, detail="Job not found") from exc
    except JobNotCompletedError as exc:
        raise HTTPException(status_code=400, detail="Job not completed") from exc
    except JobOutputMissingError as exc:
        raise HTTPException(status_code=404, detail="Output not found") from exc

    return FileResponse(output_path, filename="output.csv")
