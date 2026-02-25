from fastapi import FastAPI
from celery import Celery

app = FastAPI()

celery_app = Celery(
    "worker", 
    broker="redis://localhost:6379/0",
    backend="redis://localhost:6379/0",
)


celery_app.conf.task_routes = {
    "app.tasks.heavy_computation": {"queue": "cpu_queue"},
}