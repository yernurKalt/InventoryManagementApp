from fastapi import APIRouter, Depends

from app.api.deps import require_admin
from app.models.user import UserModel


router = APIRouter(
    prefix="/stock-movements",
    tags=["stock movements"]
)


@router.post("")
async def create_in_or_out_movement(admin_user: UserModel = Depends(require_admin)):
    pass

@router.get("")
async def get_movements():
    pass

@router.get("{id}")
async def get_movement(id: int):
    pass