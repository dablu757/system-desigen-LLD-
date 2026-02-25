from main import celery_app
import time

@celery_app.task
def heavy_computation(number: int):
    time.sleep(10)  # simulate heavy work
    return number * number