from app.tasks.celery_app import celery


@celery.task
def capture_price_snapshot(platform: str, product_id: str, lat: float, lng: float):
    # TODO: fetch current price via adapter and store in price_snapshots table
    pass
