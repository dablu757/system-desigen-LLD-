from __future__ import annotations

import os
import uuid
from pathlib import Path


class LocalFileStorage:
    def __init__(self, base_dir: str) -> None:
        self.base_dir = Path(base_dir)
        self.base_dir.mkdir(parents=True, exist_ok=True)

    def save_upload(self, filename: str, file_content: bytes) -> str:
        suffix = Path(filename).suffix or ".xlsx"
        target = self.base_dir / f"upload_{uuid.uuid4().hex}{suffix}"
        with target.open("wb") as f:
            f.write(file_content)
        return str(target)

    def build_output_path(self, job_id: str) -> str:
        target = self.base_dir / f"output_{job_id}.csv"
        return str(target)

    def ensure_path(self, path: str) -> str:
        os.makedirs(os.path.dirname(path), exist_ok=True)
        return path
