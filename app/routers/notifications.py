from fastapi import APIRouter, Depends, HTTPException, Query, status
from starlette.status import HTTP_404_NOT_FOUND

from app.api.deps import get_current_user, require_admin
from app.dao.notifications_dao import NotificationsDAO
from app.models.user import UserModel
from app.schemas.notification import NotificationOut
from app.services.pagination_response import pagination_response


router = APIRouter(
    prefix="/notifications",
    tags=["notifications"]
)


@router.get("")
async def get_all_notifications(
    size: int = Query(20, ge=1, le=100),
    page: int = Query(0, ge=0),
    current_user: UserModel = Depends(get_current_user)
):
    notifications = await NotificationsDAO.get_all_models()
    result = []
    for notification in notifications:
        result.append(NotificationOut.model_validate(notification))
    return pagination_response(arr=result, size=size, page=page)

@router.get("/{id}")
async def get_notification(id: int, current_user: UserModel = Depends(get_current_user)):
    notification = await NotificationsDAO.get_model_by_id(id=id)
    if notification is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Notification is not found",
            headers={"WWW-Authenticate": "Bearer"}
        )
    if notification.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="This notification does not belong to the current user",
            headers={"WWW-Authenticate": "Bearer"}
        )
    return NotificationOut.model_validate(notification).model_dump()
    

@router.patch("/{id}/read")
async def read_notification(id: int, current_user: UserModel = Depends(get_current_user)):
    notification = await NotificationsDAO.read_notification(id=id)
    if notification is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Notification is not found",
            headers={"WWW-Authenticate": "Bearer"}
        )
    return notification
    

@router.post("/read-all")
async def read_all_notifications(current_user: UserModel = Depends(get_current_user)):
    notifications = await NotificationsDAO.read_all_notifications_for_user(user_id=current_user.id)
    if not notifications:
        raise HTTPException(
            status_code=HTTP_404_NOT_FOUND,
            detail="Current user does not have any notifications",
            headers={"WWW-Authenticate": "Bearer"}
        )
    result = []
    for notification in notifications:
        result.append(NotificationOut.model_validate(notification).model_dump)
    return result

@router.delete("")
async def delete_all_notification(current_user: UserModel = Depends(require_admin)):
    notifications = await NotificationsDAO.get_all_models()
    for notification in notifications:
        await NotificationsDAO.delete_model_from_db(notification.id)