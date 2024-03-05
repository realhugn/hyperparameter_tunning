import json
from entities.models import Result
import config
from mq import redis, celery_execute

def run_training_bg(task_id: str, data: Result):
    try:
        data_dump = json.dumps(data.__dict__)
        redis.set(task_id, data_dump)
        # print(config.ML_QUERY_NAME, config.ML_OBJECT_DETECTION_TASK)
        celery_execute.send_task(
            name="{}.{}".format(config.celery_query, config.task_name),
            task_id = task_id,
            kwargs={
                'task_id': task_id,
                'data': data_dump,
            },
            queue= "mnist_ml"
        )
    except Exception as e:
        data.status = "FAILED"
        data.error = str(e)
        redis.set(task_id, json.dumps(data.__dict__))