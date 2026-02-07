from rq import Connection, Queue, Worker

from app.database import get_redis
from app.settings import settings


if __name__ == "__main__":
    redis_client = get_redis()
    with Connection(redis_client):
        worker = Worker([Queue(settings.queue_name)])
        worker.work()
