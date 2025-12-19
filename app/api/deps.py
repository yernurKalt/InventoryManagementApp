from fastapi import Depends, HTTPException, status
from sqlalchemy import select
from app.core.security.tokens import decode_and_validate_token
from app.db.db import async_session_maker
from app.models.user import UserModel
from app.schemas.auth import TokenPayload


async def get_current_user(token_data: TokenPayload = Depends(decode_and_validate_token)) -> UserModel:
    async with async_session_maker() as session:
        result = await session.execute(select(UserModel).where(UserModel.id == token_data.sub))
        user = result.scalar_one_or_none()
        

        if user is None:
            print("HELLO WORLD")
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="user not found",
                headers={"WWW_Authenticate": "Bearer"}
            )
        if not user.is_active:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="User is inactive"
            )
        return user

async def require_admin(user: UserModel = Depends(get_current_user)):
    if user.role != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You do not have access here, admin role is required.",
            headers={"WWW-Authenticate": "Bearer."}
        )
    return user

