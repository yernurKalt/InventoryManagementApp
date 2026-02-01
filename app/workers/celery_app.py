import os
from celery import Celery

from app.db.config import settings

REDIS_URL = settings.REDIS_URL_VALUE

app = Celery(
    "ims_worker",
    broker=REDIS_URL,
    backend=REDIS_URL,
    include=["app.workers.tasks"]
)

app.conf.update(
    task_serializer="json",
    accept_content=["json"],
    result_serializer="json",
    timezone="UTC",
    enable_utc=True,
)