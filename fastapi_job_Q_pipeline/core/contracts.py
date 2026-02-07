from __future__ import annotations

from typing import Any, Dict, Optional, Protocol


class JobRepositoryContract(Protocol):
    def create_job(self, job_id: str, data: Dict[str, Any]) -> None:
        ...

    def update_job(self, job_id: str, data: Dict[str, Any]) -> None:
        ...

    def get_job(self, job_id: str) -> Optional[Dict[str, Any]]:
        ...


class FileStorageContract(Protocol):
    def save_upload(self, filename: str, file_content: bytes) -> str:
        ...

    def build_output_path(self, job_id: str) -> str:
        ...

    def ensure_path(self, path: str) -> str:
        ...


class JobQueueContract(Protocol):
    def enqueue(self, job_id: str) -> None:
        ...


class PipelineExecutorContract(Protocol):
    def run(
        self,
        context: Dict[str, Any],
        enabled: Optional[list[str]] = None,
        order: Optional[list[str]] = None,
        parallel_groups: Optional[list[list[str]]] = None,
    ) -> Dict[str, Any]:
        ...


class CompletionNotifierContract(Protocol):
    def notify(self, callback_url: Optional[str], job_id: str, payload: Dict[str, Any]) -> None:
        ...
