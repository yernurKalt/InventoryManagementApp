from fastapi import APIRouter, Depends, HTTPException, status

from app.api.deps import get_current_user
from app.dao.product_dao import ProductDAO
from app.dao.stock_movement_dao import StockMovementDAO
from app.models.user import UserModel
from app.schemas.stockMovement import StockMovementCreate, StockMovementOut
from app.services.stock_movement_service import stock_movement_service


router = APIRouter(
    prefix="/stock-movements",
    tags=["stock movements"]
)


@router.post("")
async def create_movement(stock_movement: StockMovementCreate,current_user: UserModel = Depends(get_current_user)):
    await stock_movement_service(stock_movement)
    stock_movement = await StockMovementDAO.add_model(current_user_id=current_user.id, **stock_movement.model_dump())
    stock_movement = StockMovementOut.model_validate(stock_movement)
    return stock_movement.model_dump()

    

@router.get("")
async def get_movements(current_user: UserModel = Depends(get_current_user)):
    pass

@router.get("{id}")
async def get_movement(id: int, current_user: UserModel = Depends(get_current_user)):
    pass