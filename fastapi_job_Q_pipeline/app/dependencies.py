from __future__ import annotations

from app.database import get_redis
from app.services import JobProcessingService, JobQueryService, JobSubmissionService
from app.settings import settings
from core.executors import PipelineExecutor
from infrastructure.file_storage import LocalFileStorage
from infrastructure.notifier import HttpCallbackNotifier
from infrastructure.queue import RQJobQueue
from infrastructure.repository import RedisJobRepository


def get_submission_service() -> JobSubmissionService:
    redis_client = get_redis()
    repository = RedisJobRepository(redis_client)
    storage = LocalFileStorage(settings.storage_dir)
    queue = RQJobQueue(settings.queue_name, redis_client, settings.worker_task_path)
    return JobSubmissionService(repository, storage, queue)


def get_query_service() -> JobQueryService:
    repository = RedisJobRepository(get_redis())
    return JobQueryService(repository)


def get_processing_service() -> JobProcessingService:
    repository = RedisJobRepository(get_redis())
    storage = LocalFileStorage(settings.storage_dir)
    executor = PipelineExecutor()
    notifier = HttpCallbackNotifier()
    return JobProcessingService(repository, storage, executor, notifier)
