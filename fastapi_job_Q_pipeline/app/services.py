from __future__ import annotations

import traceback
import uuid
from typing import Any, Callable, Dict, Optional

from core.contracts import (
    CompletionNotifierContract,
    FileStorageContract,
    JobQueueContract,
    JobRepositoryContract,
    PipelineExecutorContract,
)


class JobNotFoundError(Exception):
    pass


class JobNotCompletedError(Exception):
    pass


class JobOutputMissingError(Exception):
    pass


class JobSubmissionService:
    def __init__(
        self,
        repository: JobRepositoryContract,
        storage: FileStorageContract,
        queue: JobQueueContract,
        job_id_provider: Optional[Callable[[], str]] = None,
    ):
        self.repository = repository
        self.storage = storage
        self.queue = queue
        self.job_id_provider = job_id_provider or (lambda: uuid.uuid4().hex)

    def submit(
        self,
        filename: str,
        file_content: bytes,
        pipeline_config: Optional[Dict[str, Any]],
        callback_url: Optional[str],
    ) -> str:
        job_id = self.job_id_provider()
        input_path = self.storage.save_upload(filename, file_content)
        self.repository.create_job(
            job_id,
            {
                "input_path": input_path,
                "pipeline_config": pipeline_config,
                "callback_url": callback_url,
            },
        )
        self.queue.enqueue(job_id)
        return job_id


class JobQueryService:
    def __init__(self, repository: JobRepositoryContract):
        self.repository = repository

    def get_job(self, job_id: str) -> Dict[str, Any]:
        job = self.repository.get_job(job_id)
        if not job:
            raise JobNotFoundError(f"Job '{job_id}' not found")
        return job

    def get_result_path(self, job_id: str) -> str:
        job = self.get_job(job_id)
        if job.get("status") != "COMPLETED":
            raise JobNotCompletedError(f"Job '{job_id}' is not completed")

        result = job.get("result") or {}
        output_path = result.get("output_path")
        if not output_path:
            raise JobOutputMissingError(f"Output for job '{job_id}' not found")
        return output_path


class JobProcessingService:
    def __init__(
        self,
        repository: JobRepositoryContract,
        storage: FileStorageContract,
        executor: PipelineExecutorContract,
        notifier: CompletionNotifierContract,
    ):
        self.repository = repository
        self.storage = storage
        self.executor = executor
        self.notifier = notifier

    def process(self, job_id: str) -> None:
        job = self.repository.get_job(job_id)
        if not job:
            return

        self.repository.update_job(job_id, {"status": "RUNNING"})

        try:
            output_path = self.storage.build_output_path(job_id)
            self.storage.ensure_path(output_path)

            pipeline_config = job.get("pipeline_config") or {}
            enabled = pipeline_config.get("enabled_stages")
            order = pipeline_config.get("order")
            parallel_groups = pipeline_config.get("parallel_groups")

            context = {
                "job_id": job_id,
                "input_path": job["input_path"],
                "output_path": output_path,
            }

            results = self.executor.run(
                context=context,
                enabled=enabled,
                order=order,
                parallel_groups=parallel_groups,
            )

            result_payload: Dict[str, Any] = {
                "output_path": output_path,
                "stages": list(results.keys()),
            }
            self.repository.update_job(job_id, {"status": "COMPLETED", "result": result_payload})
            self.notifier.notify(job.get("callback_url"), job_id, result_payload)

        except Exception as exc:  # noqa: BLE001 - track worker errors in job metadata
            error_payload = {
                "status": "FAILED",
                "error": str(exc),
                "traceback": traceback.format_exc(),
            }
            self.repository.update_job(job_id, error_payload)
            self.notifier.notify(job.get("callback_url"), job_id, {"status": "FAILED", "error": str(exc)})
