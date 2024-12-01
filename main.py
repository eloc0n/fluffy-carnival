import time

from config.settings import settings
from config.database import Database
import uvicorn as uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from config.celery_utils import create_celery
from routers import universities


app = FastAPI(
    title="Asynchronous tasks processing with Celery and RabbitMQ",
    description="Sample FastAPI Application to demonstrate Event "
    "driven architecture with Celery and RabbitMQ",
    version="1.0.0",
)

app.celery_app = create_celery()
db = Database(db_url=str(settings.SQLALCHEMY_DATABASE_URI))
app.database = db
app.include_router(universities.router)

# CORS configuration
app.add_middleware(
    CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"]
)

celery = app.celery_app
database = app.database


@app.middleware("http")
async def add_process_time_header(request, call_next):
    print("inside middleware!")
    start_time = time.time()
    response = await call_next(request)
    process_time = time.time() - start_time
    response.headers["X-Process-Time"] = str(f"{process_time:0.4f} sec")
    return response
