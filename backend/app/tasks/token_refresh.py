from app.tasks.celery_app import celery


@celery.task
def refresh_expiring_tokens():
    # TODO: query platform_accounts where token_expires_at < now + 10 minutes
    # For each, call adapter.refresh_auth() and update the encrypted tokens
    pass
