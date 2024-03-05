from redis import Redis
from redis.exceptions import ConnectionError
from kombu import Connection
from settings import config
from kombu.exceptions import OperationalError


def is_redis_running() -> bool:
    try:
        conn = Redis(
            host=config.redis_host, 
            port=config.redis_port, 
            password=config.redis_pass,
            db= config.redis_db
        )
        print(conn)
        conn.client_list()  # Must perform an operation to check connection.
    except ConnectionError as e:
        print("Failed to connect to Redis instances")
        print(repr(e))
        return False
    conn.close()
    return True



def is_rbmq_running(retries: int = 3) -> bool:
    try:
        print(config.broker)
        conn = Connection(config.broker)
        conn.ensure_connection(max_retries=retries)
    except OperationalError as e:
        print("Failed to connect to RabbitMQ instance")
        print(str(e))
        return False
    conn.close()
    return True