from fastapi import FastAPI
import asyncio
from pydantic import BaseModel

from fastapi.concurrency import run_in_threadpool
'''
run_in_threadpool is a utility function that allows 
you to run blocking (sync) code inside a separate thread, 
without blocking FastAPI's event loop.

'''

from redis import Redis
from rq import Queue


from io_tasks import async_io_task
from cpu_tasks import cpu_heavy_task
from job import print_number

app = FastAPI(
    title="fastapi concurrency demo"
)

#redis connection
redis_connection = Redis(
    host='localhost',
    port=6379
)

#task queue
task_queue = Queue(
    'task_queue',
    connection=redis_connection
)

class JobRequest(BaseModel):
    lowest : int
    highest : int

#route
@app.get('/')
def health():
    return{
        'sucess' : True,
        'message' : 'pong'
    }

@app.get('/io')
async def io_concurrency():
    task = [async_io_task(i) for i in range(5)]
    result = await asyncio.gather(*task)
    return{
        "type" :"io_concurrency",
        "result" :result
    }

@app.post('/job')
def post_job(jobR:JobRequest):
    l = jobR.lowest
    h = jobR.highest

    job_instance=task_queue.enqueue(print_number,l, h)

    return {
        'success' : True,
        'id' : job_instance.id
    }


