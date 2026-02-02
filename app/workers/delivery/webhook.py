import httpx

from app.db.config import settings

WEBHOOK_URL = settings.WEBHOOK_URL_VALUE


def send_webhook(payload: dict) -> None:
    if not WEBHOOK_URL:
        raise RuntimeError("WebHook is not set")

    with httpx.Client(timeout=10.0) as client:
        print(payload)
        print("there is the mistake")
        resp = client.post(WEBHOOK_URL, json=payload)

    if resp.status_code < 200 or resp.status_code >= 300:
        raise RuntimeError(f"Webhook failed: status={resp.status_code}, body={resp.text}")