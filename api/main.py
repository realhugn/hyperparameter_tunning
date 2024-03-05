import asyncio
from celery.result import AsyncResult
from fastapi import FastAPI, Request, WebSocket, WebSocketDisconnect
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
import uvicorn
from fastapi.middleware.cors import CORSMiddleware
from train_task.router import router
from database.connect import engine
import schema
import config

schema.Base.metadata.create_all(bind=engine)
#create our app instance
app = FastAPI(openapi_url='/api/v1/openapi.json', docs_url='/api/v1/docs')
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
    allow_credentials=True
)


# real_path = os.path.realpath(__file__)
# dir_path = os.path.dirname(real_path)
# LOGFILE = f"{dir_path}/test.log"
# async def logGenerator(request):
#     for line in tail("-f", LOGFILE, _iter=True):
#         if await request.is_disconnected():
#             print("client disconnected!!!")
#             break
#         yield line
#         time.sleep(0.5)

# @app.get('/stream-logs')
# async def runStatus(request: Request):
#     event_generator = logGenerator(request)
#     return EventSourceResponse(event_generator)
app.include_router(router, prefix='/api/v1')

@app.get("/")
def home(request: Request):
    return templates.TemplateResponse("home.html", context={"request": request})

@app.get("/{task_id}")
def home(request: Request, task_id: str):
    return templates.TemplateResponse("detail.html", context={"request": request, "task_id": task_id, "host": config.host})
