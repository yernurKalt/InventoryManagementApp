from datetime import datetime, timezone
from fastapi import APIRouter, Request



router = APIRouter(
    prefix="/dev/webhook",
    tags=["webhook"]
)

@router.post("")
async def webhook(request: Request):
    print("some error occured")
    payload = await request.json()

    print("\n========== WEBHOOK RECEIVED ==========")
    print("Time:", datetime.now(timezone.utc).isoformat())
    print("Payload:", payload)
    print("======================================\n")

    return {"ok": True, "received": payload}