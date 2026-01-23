import httpx

WEBHOOK_URL = "http://127.0.0.1:8000/dev/webhook"


def send_webhook(payload: dict) -> None:
    if not WEBHOOK_URL:
        raise RuntimeError("WebHook is not set")

    with httpx.Client(timeout=10.0) as client:
        resp = client.post(WEBHOOK_URL, json=payload)

    if resp.status_code < 200 or resp.status_code >= 300:
        raise RuntimeError(f"Webhook failed: status={resp.status_code}, body={resp.text}")