from asyncio import tasks

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from starlette.responses import JSONResponse

from routes import users, task
from utils.database import engine
from models import models
import logging
logging.basicConfig(level=logging.DEBUG)



app = FastAPI(title="KanbanGPT")
app.include_router(users.router, prefix="/api", tags=["Users"])
app.include_router(task.router, prefix="/api", tags=["Tasks"])



origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# @app.middleware("http")
# async def exception_handling(request: Request, call_next):
#     try:
#         return await call_next(request)
#     except Exception as exc:
#         return JSONResponse(status_code=500, content='Error occurred: {}'.format(exc))


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/ping")
async def root():
    return "Pong"
