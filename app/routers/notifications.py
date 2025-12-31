from fastapi import APIRouter


router = APIRouter(
    prefix="/notifications",
    tags=["notifications"]
)


@router.get("")
async def get_all_notifications():
    pass

@router.get("/{id}")
async def get_notification(id: int):
    pass

@router.patch("/{id}/read")
async def read_notification(id: int):
    pass

@router.post("/read-all")
async def read_all_notifications():
    pass