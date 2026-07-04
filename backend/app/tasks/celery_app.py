from celery import Celery

from app.config import settings

celery = Celery("mycart", broker=settings.redis_url, backend=settings.redis_url)

celery.conf.update(
    task_serializer="json",
    accept_content=["json"],
    result_serializer="json",
    timezone="Asia/Kolkata",
    enable_utc=True,
    beat_schedule={
        "refresh-expiring-tokens": {
            "task": "app.tasks.token_refresh.refresh_expiring_tokens",
            "schedule": 300.0,  # every 5 minutes
        },
    },
)
