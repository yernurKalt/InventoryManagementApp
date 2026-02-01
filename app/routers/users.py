from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select

from app.api.deps import get_current_user, require_admin
from app.core.security.password import hash_password
from app.dao.user_dao import create_user, deactivate_user_by_id, get_user_by_email
from app.db.db import async_session_maker
from app.models.user import UserModel
from app.schemas.user import UserCreate, UserOut


router = APIRouter(
    prefix="/users",
    tags=["users"]
)


@router.post("")
async def create_employee_accounts(
    user: UserCreate,
    current_user: UserModel = Depends(require_admin),
    ):
    async with async_session_maker() as session:
        old_user = await get_user_by_email(user.email)
        if old_user:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="User already exists",
                headers={"WWW-Authenticate": "Bearer"}
            )
        result = await create_user(**user.model_dump())
        user = UserOut.model_validate(result)
        return user.model_dump()

@router.post("/admin_user")
async def create_admin_user(user: UserCreate):
    async with async_session_maker() as session:
        old_user = await get_user_by_email(user.email)
        if old_user:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="User already exists",
                headers={"WWW-Authenticate": "Bearer"}
            )
        result = await create_user(**user.model_dump())
        user = UserOut.model_validate(result)
        return user.model_dump()

@router.get("/me")
async def me(current_user: UserModel = Depends(get_current_user)):
    user = UserOut.model_validate(current_user)
    return user.model_dump()


@router.patch("/{id}/deactivate")
async def deactivate_user(id: int, current_user: UserModel = Depends(require_admin)):
    await deactivate_user_by_id(id)
    return {"message": "user now is inactive"}