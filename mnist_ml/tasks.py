import json
from celery import Celery
import time as t
from celery.utils.log import get_task_logger
from mq import redis
from check import is_rbmq_running, is_redis_running
from ml.main import run_training
from settings import celery_config, config



if not is_redis_running(): exit()
if not is_rbmq_running(): exit()

app = Celery("mnist_ml", broker=config.broker, backend=config.redis_backend)
app.config_from_object(celery_config)
# Create logger - enable to display messages on task logger
celery_log = get_task_logger(__name__)


@app.task(bind=True, name="{query}.{task_name}".format(
              query=celery_config.QUERY_NAME, 
              task_name=celery_config.TASK_NAME))
def train_model(self, task_id: str, data: bytes): 

    data = json.loads(data)
    channel = '_'.join(['task', task_id])
    message_init = {"msg" : "init task" + task_id}
    redis.publish(channel, json.dumps(message_init))
    lr, momentum, epochs, batch_size =data["lr"], data["momentum"], data["epochs"], data["batch_size"]
    acc, f1, time = run_training(lr, momentum, epochs, batch_size, task_id, channel)
    data["acc"] = acc
    data["f1"] = f1
    data["time"] = time
    data["status"] = "SUCCESS"
    data["done_time"] = t.time()
    
    data_dump = json.dumps(data)
    celery_log.info(f"Celery task completed!")
    redis.set(task_id, data_dump) 