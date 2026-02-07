from __future__ import annotations

from app.dependencies import get_processing_service


def run_pipeline_job(job_id: str) -> None:
    processing_service = get_processing_service()
    processing_service.process(job_id)
