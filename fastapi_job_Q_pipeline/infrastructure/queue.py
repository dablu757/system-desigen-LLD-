from __future__ import annotations

import redis
from rq import Queue


class RQJobQueue:
    def __init__(self, queue_name: str, redis_client: redis.Redis, task_path: str):
        self.queue_name = queue_name
        self.redis_client = redis_client
        self.task_path = task_path

    def enqueue(self, job_id: str) -> None:
        queue = Queue(self.queue_name, connection=self.redis_client)
        queue.enqueue(self.task_path, job_id)
