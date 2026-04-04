from celery import Celery
from celery.schedules import crontab

from backend.core.config import settings


redis_url = (
    f"redis://:{settings.REDIS_PASSWORD}@{settings.REDIS_HOST}:{settings.REDIS_PORT}/0"
)

celery_app = Celery("backend", broker=redis_url, backend=redis_url)

celery_app.autodiscover_tasks(["backend.infrastructure.celery.tasks"])

celery_app.conf.beat_schedule = {
    "expire-orders": {
        "task": "backend.infrastructure.celery.tasks.tasks.expire_orders",
        "schedule": crontab(minute=f"*/{settings.PENDING_STATUS_UPDATE_EVERY}"),
    },
}

celery_app.conf.timezone = "UTC"
