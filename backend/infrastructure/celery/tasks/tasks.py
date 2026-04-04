from sqlalchemy import text

from backend.db.sync_db import get_sync_engine
from backend.infrastructure.celery.celery_app import celery_app


@celery_app.task
def expire_orders():

    engine = get_sync_engine()

    with engine.begin() as conn:
        conn.execute(
            text(
                """
                UPDATE "order"
                SET status = 'expired'
                WHERE status = 'pending'
                AND expires_at < now()
                """
            )
        )


