from fastapi import APIRouter, Depends, HTTPException, status

from app.api.deps import get_current_user
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
    movement = await StockMovementDAO.get_model_by_id(id)
    if movement is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Movement is not found"
        )
    return StockMovementOut.model_validate(movement).model_dump()