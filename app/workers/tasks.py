from datetime import datetime, timezone

from celery import states
from app.models.notification import NotificationModel
from app.workers.celery_app import app
from app.workers.db_sync import get_sync_session
from app.workers.delivery.webhook import send_webhook


@app.task(name="send_notification", bind=True, max_retries=3)
def send_notification(self, noitification_id: int) -> str:
    session = get_sync_session()
    try:
        
        notif = session.get(NotificationModel, noitification_id)
        if not notif:
            return "noop:not_found"
        
        if getattr(notif, "status", None) == "sent":
            return "noop:already_sent"
        
        payload = {
            "id": notif.id,
            "type": notif.type,
            "message": notif.message,
            "user_id": notif.user_id,
            "product_id": getattr(notif, "product_id", None),
            "created_at": notif.created_at.isoformat() if notif.created_at else None,
        }
        send_webhook(payload)
        notif.status = "sent"
        notif.sent_at = datetime.now(timezone.utc)
        session.commit()
        return "ok:sent"
    except Exception as exc:
        session.rollback()

        try:
            countdown = 10 * (3 ** self.request.retries)
            raise self.retry(exc=exc, countdown=countdown)
        except self.MaxRetriesExceededError:
            notif = session.get(NotificationModel, noitification_id)
            if notif:
                notif.status = "failed"
                session.commit()

            self.update_state(state=states.FAILURE, meta={"error": str(exc)})
            return "Failed"

    finally:
        session.close()