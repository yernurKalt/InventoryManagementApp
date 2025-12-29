from fastapi import HTTPException, status
from app.dao.product_dao import ProductDAO
from app.schemas.stockMovement import StockMovementCreate


async def stock_movement_service(new_movement: StockMovementCreate):
    if new_movement.quantity <= 0:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_CONTENT,
            detail="Quantity must be greater than 0",
            headers={"WWW-Authenticate": "Bearer"}
        )
    
    product = await ProductDAO.get_model_by_id(new_movement.product_id)
    if product is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Product is not found",
            headers={"WWW-Authenticate": "Bearer"}
        )
    if new_movement.movement_type != "OUT" and new_movement.movement_type != "IN":
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_CONTENT,
            detail="movement should be either \"IN\" or \"OUT\"",
            headers={"WWW-Authenticate": "Bearer"}
        )
    if new_movement.movement_type == "OUT":
        if product.current_stock < new_movement.quantity:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail=f"current stock of the product with id {new_movement.product_id} is less than the requested amount of product",
                headers={"WWW-Authenticate": "Bearer"}
            )
        new_stock = product.current_stock - new_movement.quantity
        await ProductDAO.update_current_stock(product.id, new_stock)
    if new_movement.movement_type == "IN":
        new_stock = product.current_stock + new_movement.quantity
        await ProductDAO.update_current_stock(product.id, new_stock)