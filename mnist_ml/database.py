from sqlalchemy import create_engine
from sqlalchemy.engine import URL
from sqlalchemy.pool import NullPool
from settings import config

url = URL.create(
    drivername=config.driver,
    username=config.db_user,
    host=config.db_host,
    password=config.db_pass,
    database=config.db_name,
    port=config.db_port
)

engine = create_engine(
    url, echo=True, poolclass=NullPool
)