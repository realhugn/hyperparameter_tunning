import time
import torch
from torch import nn, tensor
from torchvision import transforms
from torchvision import datasets as dts
from sqlalchemy.orm import Session
from database import engine
from sklearn.metrics import f1_score 
from schema import Job
from .ml_model import classicationmodel
from celery.utils.log import get_task_logger
from mq import redis
import json


celery_log = get_task_logger(__name__)

def run_training(lr=3e-3, momentum=0.9, epochs=10, batch_size = 10, task_id = None, channel = None) :
    session = Session(engine)
    start_time = time.time()
    trnsform = transforms.Compose([transforms.ToTensor(), transforms.Normalize((0.5,), (0.5,)),])

    train_set = dts.MNIST(root='./dataset', train=True, transform=trnsform ,download=True)
    train_data_loader = torch.utils.data.DataLoader(train_set, batch_size, shuffle=True)

    test_set = dts.MNIST(root='./dataset', train=False, transform=trnsform, download=True)
    test_data_loader = torch.utils.data.DataLoader(test_set, batch_size, shuffle=True)
    celery_log.info(f"Data prepared")
    redis.publish(channel, message=json.dumps({"msg": f"Data prepared"}))
    cmodel = classicationmodel()
    loss_fn = nn.CrossEntropyLoss()
    optimizer = torch.optim.SGD(cmodel.parameters(),lr , momentum)
    redis.publish(channel, message=json.dumps({"msg": f"Model prepared"}))
    celery_log.info(f"Model prepared")
    session.query(Job).filter(Job.task_id==task_id).update({Job.status: "RUNNING"})
    session.commit()
    cmodel.train()
    celery_log.info(f"Start training")
    for epoch in range(epochs):
        for batch, (X, y) in enumerate(train_data_loader):
            X = X.reshape(-1, 28*28)
            y_pred = cmodel(X)
            loss = loss_fn(y_pred, y)
            optimizer.zero_grad()
            loss.backward()
            optimizer.step()
            if ( batch + 1) % 100 == 0:
                redis.publish(channel, message=json.dumps({"msg": f'Epochs [{epoch+1}/{epochs}], Step[{batch+1}/{len(train_data_loader)}], Losses: {loss.item():.4f}'}))
                celery_log.info(f'Epochs [{epoch+1}/{epochs}], Step[{batch+1}/{len(train_data_loader)}], Losses: {loss.item():.4f}')
    celery_log.info('Training task completed')
    redis.publish(channel, message=json.dumps({"msg": f"Training task completed"}))

    celery_log.info('Start evaluate')
    redis.publish(channel, message=json.dumps({"msg": f"Start evaluate"}))

    cmodel.eval()
    size = 0
    batch_accuracy = {}
    true = 0
    _true = 0
    _batch_size = 0
    pred_all = tensor([])
    true_all = tensor([])
    with torch.no_grad():
        for batch , (X, y) in enumerate(test_data_loader):
            X = X.reshape(-1, 28*28)
            pred = cmodel(X)
            pred_all = torch.cat((pred_all, pred.argmax(1)))
            true_all = torch.cat((true_all, y))
            _batch_size = len(X)
            
            _true = (pred.argmax(1) == y).type(torch.float).sum().item()
            true += _true
            
            size+=_batch_size
            batch_accuracy[batch] = _true/_batch_size
    true /= size
    f1 = f1_score(true_all, pred_all, average="micro")
    redis.publish(channel, message=json.dumps({"msg": f"Valid Error: \n Accuracy: {(100*true):>0.1f}%, F1: {f1:>8f} \n"}))
    celery_log.info(f"Valid Error: \n Accuracy: {(100*true):>0.1f}%, F1: {f1:>8f} \n")
    celery_log.info("Eval task completed")
    redis.publish(channel, message=json.dumps({"msg": f"Eval task completed"}))
    session.query(Job).filter(Job.task_id==task_id).update({Job.f1: f1,Job.acc: true*100, Job.time: time.time()- start_time , Job.status: "SUCCESS"})
    session.commit()
    session.close()
    return true*100, f1, start_time - time.time()
    
