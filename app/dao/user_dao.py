from sqlalchemy import select
from app.core.security.password import hash_password
from app.db.db import async_session_maker
from app.models.user import UserModel
from app.schemas.user import UserOut


async def get_user_by_email(email: str) -> UserModel:
    async with async_session_maker() as session:
        result = await session.execute(select(UserModel).where(UserModel.email == email))
        user = result.scalar_one_or_none()
        return user


async def deactivate_user_by_id(id: int) -> UserModel:
    async with async_session_maker() as session:
        result = await session.execute(select(UserModel).where(UserModel.id == id))
        user = result.scalar_one_or_none()
        if user:
            user.is_active = False
            await session.commit()



async def create_user(
    email: str,
    full_name: str,
    password: str,
    role: str = "employee",
    is_active: bool=True,
    ):
    async with async_session_maker() as session:
        user = UserModel(
            email=email,
            full_name=full_name,
            hashed_password=hash_password(password),
            role=role,
            is_active=is_active
        )
        session.add(user)
        await session.commit()
        return user