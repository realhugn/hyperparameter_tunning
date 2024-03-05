from redis import Redis
from celery import Celery
import config


redis = Redis(host=config.redis_host,
              port=config.redis_port,
              password= config.redis_pass, 
              db=config.redis_db)
redis_sub = redis.pubsub()


celery_execute = Celery(broker=config.broker, backend=config.redis_backend)