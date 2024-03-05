from pydantic import BaseModel
from typing import Optional
import time

class RequestData(BaseModel):
    lr: float
    momentum: float
    epochs: int
    batch_size: int


class Task(BaseModel):
    # Celery task representation
    task_id: str
    status: str

class Metrics(BaseModel): 
    acc: float = 0.
    time: int = time.time()
    f1: float = 0.

class Result(BaseModel):
    task_id: str
    lr: float
    momentum: float
    epochs: int
    batch_size: int
    acc: float = 0.
    f1: float = 0.
    status: str
    time: int = time.time()

    
    