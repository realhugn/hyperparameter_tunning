from redis import Redis
from settings import config

redis = Redis(
    host=config.redis_host, 
    port=config.redis_port, 
    password=config.redis_pass,
    db= config.redis_db
)