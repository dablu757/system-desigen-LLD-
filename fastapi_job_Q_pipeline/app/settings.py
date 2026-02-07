import os
from pydantic import BaseModel


class Settings(BaseModel):
    redis_url: str = os.getenv("REDIS_URL", "redis://localhost:6379/0")
    storage_dir: str = os.getenv("STORAGE_DIR", "./storage")
    queue_name: str = os.getenv("QUEUE_NAME", "pipeline-jobs")
    worker_task_path: str = os.getenv("WORKER_TASK_PATH", "app.tasks.run_pipeline_job")


settings = Settings()
