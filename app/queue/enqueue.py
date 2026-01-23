from app.workers.tasks import send_notification

def enqueue_send_notification(notification_id: int) -> str:
    job = send_notification.delay(notification_id)
    return job.id 