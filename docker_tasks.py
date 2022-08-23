'''docker_tasks.py
Queues the data_downloader using Redis queue.'''
from redis import Redis
from rq import Queue
from rq_scheduler import Scheduler
from data_downloader import run
queue = Queue("pentryansvar_data", connection=Redis()) #Create a Redis queue
scheduler = Scheduler(queue=queue)
scheduler.cron(
    "0 1 * * *",
    func=run,
    repeat=None,
    queue_name="pentryansvar_data",
    use_local_timezone=True
)