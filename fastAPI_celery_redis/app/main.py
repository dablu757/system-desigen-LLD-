from fastapi import FastAPI
from task import heavy_computation
from celery.result import AsyncResult
from celery_app import celery_app

app = FastAPI()


@app.post("/calculate/{number}")
def calculate(number: int):
    task = heavy_computation.delay(number)
    return {"task_id": task.id}


@app.get("/status/{task_id}")
def get_status(task_id: str):
    task_result = AsyncResult(task_id, app=celery_app)

    return {
        "task_id": task_id,
        "status": task_result.status,
        "result": task_result.result if task_result.ready() else None,
    }
