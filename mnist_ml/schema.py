from sqlalchemy import TIMESTAMP, Column, String, FLOAT, INTEGER
from sqlalchemy.sql import func
from sqlalchemy.orm import declarative_base

Base = declarative_base()

class Job(Base):
    __tablename__ = 'jobs'
    task_id = Column(String, primary_key=True)
    lr = Column(FLOAT, nullable=False)
    momentum = Column(FLOAT, nullable=False)
    epochs = Column(INTEGER, nullable=True)
    batch_size = Column(INTEGER, nullable=False)
    acc = Column(FLOAT, nullable=False, default = 0.)
    f1 = Column(FLOAT, nullable=False, default = 0.)
    status = Column(String, nullable=False)
    time = Column(INTEGER, default = 99999999)