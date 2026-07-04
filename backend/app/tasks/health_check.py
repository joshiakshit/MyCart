from app.tasks.celery_app import celery


@celery.task
def check_platform_health():
    # TODO: call health_check() on each adapter, update Redis status cache
    pass
