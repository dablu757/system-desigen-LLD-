from __future__ import annotations

import traceback
from typing import Any, Dict

import requests

from app.database import get_redis
from app.settings import settings
from core.executors import PipelineExecutor
from infrastructure.file_storage import FileStorage
from infrastructure.repository import JobRepository


def run_pipeline_job(job_id: str) -> None:
    redis_client = get_redis()
    repo = JobRepository(redis_client)
    job = repo.get_job(job_id)
    if not job:
        return

    repo.update_job(job_id, {"status": "RUNNING"})
    storage = FileStorage(settings.storage_dir)
    executor = PipelineExecutor()

    try:
        input_path = job["input_path"]
        output_path = storage.build_output_path(job_id)
        storage.ensure_path(output_path)

        pipeline_config = job.get("pipeline_config") or {}
        enabled = pipeline_config.get("enabled_stages")
        order = pipeline_config.get("order")
        parallel_groups = pipeline_config.get("parallel_groups")

        context = {
            "job_id": job_id,
            "input_path": input_path,
            "output_path": output_path,
        }

        results = executor.run(
            context=context,
            enabled=enabled,
            order=order,
            parallel_groups=parallel_groups,
        )

        result_payload: Dict[str, Any] = {
            "output_path": output_path,
            "stages": list(results.keys()),
        }

        repo.update_job(job_id, {"status": "COMPLETED", "result": result_payload})

        callback_url = job.get("callback_url")
        if callback_url:
            _send_callback(callback_url, job_id, result_payload)

    except Exception as exc:  # noqa: BLE001 - capture for job status
        repo.update_job(
            job_id,
            {
                "status": "FAILED",
                "error": f"{exc}",
                "traceback": traceback.format_exc(),
            },
        )

        callback_url = job.get("callback_url")
        if callback_url:
            _send_callback(callback_url, job_id, {"error": str(exc), "status": "FAILED"})


def _send_callback(url: str, job_id: str, payload: Dict[str, Any]) -> None:
    try:
        requests.post(
            url,
            json={"job_id": job_id, "payload": payload},
            timeout=10,
        )
    except Exception:
        pass
