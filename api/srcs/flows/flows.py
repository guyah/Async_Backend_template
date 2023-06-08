from srcs.app.models import Placeholder
from srcs.tasks.celery import ManagedTask, worker
import time

@worker.task(base=ManagedTask)
async def flow_placeholder(placeholder_id: int) -> Placeholder:
    placeholder: Placeholder = await Placeholder.get(id=placeholder_id)
    time.sleep(2)
    print(f"Placeholder: {placeholder}")