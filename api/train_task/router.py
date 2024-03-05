import asyncio
import json
import uuid

from fastapi.responses import PlainTextResponse
import schema
import config
from sqlalchemy.orm import Session
from database.connect import get_db
from fastapi import APIRouter, BackgroundTasks, Depends, HTTPException, WebSocket, WebSocketDisconnect
from celery.result import AsyncResult
from .background import run_training_bg
from mq import redis, celery_execute
from entities.models import Metrics, RequestData, Result
import time
from mq import redis, redis_sub

router = APIRouter()

@router.get('/')
def touch():
    return 'API is running'

@router.post('/train', status_code=202)
async def run_training(requestData: RequestData, background_tasks: BackgroundTasks, db: Session = Depends(get_db)):

    time_now = time.time()
    task_id = str(uuid.uuid5(uuid.NAMESPACE_OID, "mnist_ml" + "_"+ str(time_now)))
    lr, momentum, epochs, batch_size = requestData.lr, requestData.momentum, requestData.epochs, requestData.batch_size
    isExist = db.query(schema.Job).filter(schema.Job.lr == lr,schema.Job.epochs == epochs,schema.Job.batch_size == batch_size,schema.Job.momentum == momentum).first()
    if isExist :
        raise HTTPException(status_code=400, detail='Job duplicated') 
    data = Result(task_id=task_id, lr=lr, momentum=momentum, epochs=epochs, batch_size=batch_size ,acc=0., f1=0., status="PENDING", time=time_now)
    init_job = schema.Job(task_id = task_id, lr = lr , momentum = momentum, epochs = epochs, batch_size = batch_size, status = "PENDING")
    db.add(init_job)
    db.commit()
    redis.set(task_id, json.dumps(data.__dict__))
    background_tasks.add_task(run_training_bg, task_id, data)
    redis_sub.subscribe("task_"+task_id)
    return {'task_id': str(task_id), 'status': 'Processing'}

@router.get("/status/{task_id}", response_model=Result)
def ml_status(
    # *,
    task_id: str,
    db: Session = Depends(get_db)
):
    data = redis.get(task_id)
    if data == None:
        data = db.query(schema.Job).filter(task_id).first()
        if data == None: 
            raise HTTPException(status_code=404, detail='task id not found!')
    message = json.loads(data)
    print(message)
    return message

@router.get("/logs/{task_id}", response_model=Result)
def ml_status(
    # *,
    task_id: str,
    db: Session = Depends(get_db)
):
    file_name = f"task_{task_id}.txt"
    file_path = f"./{file_name}"
    file = open(file_path, "r")
    return PlainTextResponse(file.read())

@router.websocket("/ws/task/{task_id}")
async def websocket_endpoint(websocket: WebSocket, task_id: str):
    await websocket.accept()

    # Get the task result asynchronously
    result = AsyncResult(task_id, app=celery_execute)
    if result.successful():
        file_name = f"task_{task_id}.txt"
        file_path = f"./{file_name}"
        file = open(file_path, "r")
        await websocket.send_text(file.read())
    else:
        await websocket.send_text(f"Task {task_id} failed: {result}")
    while True:
        data = redis_sub.get_message()
        try: 
            if(data):
                if (data['data'] != 1):
                    message = json.loads(data['data'].decode('utf-8'))['msg']
                    with open(f"task_{task_id}.txt", "a") as a_file:
                        a_file.write("\n")
                        a_file.write(message)
                    await websocket.send_text(message)
            if(result.successful()):
                break
        except WebSocketDisconnect:
            pass
    # Task is ready, send the final result



@router.get("/all")
def get_all(db: Session = Depends(get_db)):
    all =  db.query(schema.Job).all()
    return {'status': 'success', 'results': len(all), 'jobs': all}