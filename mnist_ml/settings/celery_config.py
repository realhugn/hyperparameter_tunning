from kombu import Queue
from dotenv import load_dotenv
import os

load_dotenv()

#=========================================================================
#                          CELERY INFORMATION 
#=========================================================================
task_acks_late = True
worker_prefetch_multiplier = 1

QUERY_NAME = os.getenv("CELERY_QUERY")
TASK_NAME = os.getenv("TASK_NAME")
task_queues = [Queue(name=QUERY_NAME)]
