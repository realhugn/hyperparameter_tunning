from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.engine import URL
import config

url = URL.create(
    drivername=config.driver,
    username=config.db_user,
    host=config.db_host,
    password=config.db_pass,
    database=config.db_name,
    port=config.db_port
)

engine = create_engine(
    url, echo=True
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
