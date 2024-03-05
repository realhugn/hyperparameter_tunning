from dotenv import load_dotenv
import os

load_dotenv()

# REDIS BACKEND
redis_host = os.getenv("REDIS_HOST")
redis_port = os.getenv("REDIS_PORT")
redis_pass = os.getenv("REDIS_PASS")
redis_db = os.getenv("REDIS_DB")
redis_backend = "redis://:{password}@{hostname}:{port}/{db}".format(
    hostname=redis_host,
    password=redis_pass,
    port=redis_port,
    db=redis_db
)


#RABBITMQ BROKER
rabbitmq_host=os.getenv("RABBITMQ_HOST")
rabbitmq_port=os.getenv("RABBITMQ_PORT")
rabbitmq_user=os.getenv("RABBITMQ_USER")
rabbitmq_pass=os.getenv("RABBITMQ_PASS")
rabbitmq_vhost=os.getenv("RABBITMQ_VHOST")
broker = "amqp://{user}:{pw}@{hostname}:{port}/{vhost}".format(
    user=rabbitmq_user,
    pw=rabbitmq_pass,
    hostname=rabbitmq_host,
    port=rabbitmq_port,
    vhost=rabbitmq_vhost
)


#DATABASE
driver=os.getenv("PQ_DRIVER")
db_user=os.getenv("DB_USERNAME")
db_host=os.getenv("DB_HOST")
db_pass=os.getenv("DB_PASSWORD")
db_name=os.getenv("DB_NAME")
db_port=os.getenv("DB_PORT")

#CELERY
celery_query=os.getenv("CELERY_QUERY")
task_name=os.getenv("TASK_NAME")