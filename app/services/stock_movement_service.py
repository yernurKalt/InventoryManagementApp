from fastapi import HTTPException, status
from app.dao.notifications_dao import NotificationsDAO
from app.dao.product_dao import ProductDAO
from app.dao.user_dao import get_admins_users
from app.schemas.notification import NotificationBase
from app.schemas.stockMovement import StockMovementCreate
from app.services.low_stock_service import low_stock_service


async def stock_movement_service(new_movement: StockMovementCreate):
    if new_movement.quantity <= 0:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_CONTENT,
            detail="Quantity must be greater than 0",
            headers={"WWW-Authenticate": "Bearer"}
        )
    
    product = await ProductDAO.get_model_by_id_with_lock(new_movement.product_id)
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
        if low_stock_service(product.reorder_level, product.current_stock):
            users = await get_admins_users()
            for user in users:
                dedupe_key = f"LOW_STOCK:user{user.id}:product{product.id}"
                notification = await NotificationsDAO.get_by_dedupe_key(dedupe_key)
                if notification is None:
                    new_notification = NotificationBase(
                        message=f"Low stock: {product.name} {product.sku}, current stock: {product.current_stock}, reorder level: {product.reorder_level}",
                        product_id=product.id,
                        user_id=user.id,
                        dedupe_key=dedupe_key,
                        type="LOW_STOCK"
                    )
                    await NotificationsDAO.add_model(**new_notification.model_dump())
                    
    if new_movement.movement_type == "IN":
        new_stock = product.current_stock + new_movement.quantity
        await ProductDAO.update_current_stock(product.id, new_stock)