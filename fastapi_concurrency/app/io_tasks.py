import asyncio
import httpx


async def async_io_task(task_id : int):

    async with httpx.AsyncClient() as client:
        await asyncio.sleep(2) #non blocking task

    return f"I/O taks {task_id} Done"