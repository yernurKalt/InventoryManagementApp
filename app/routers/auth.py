from datetime import timedelta
from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from sqlalchemy import select

from app.core.security.password import hash_password
from app.core.security.tokens import create_access_token
from app.db.config import settings
from app.db.db import async_session_maker
from app.models.user import UserModel
from app.schemas.auth import Token
from app.schemas.user import UserCreate


router = APIRouter(
    prefix="/auth",
    tags=["authentication"],
    )


@router.post("/login", response_model=Token)
async def login(form_data: Annotated[OAuth2PasswordRequestForm, Depends()]):
    email = form_data.username
    async with async_session_maker() as session:
        result = await session.execute(select(UserModel).where(UserModel.email == email))
        user = result.scalar_one_or_none()
        if user is None:

            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail=f"Could not find user with email {email}"
            )
        access_token_expires = timedelta(minutes=settings.EXPIRE_MINUTES)
        access_token = create_access_token(
            data={"sub": str(user.id), "role": user.role},
            expires_delta=access_token_expires
        )
        return Token(access_token=access_token, token_type="bearer")

@router.post("/register")
async def register(user: UserCreate):
    async with async_session_maker() as session:
        result = await session.execute(select(UserModel).where(UserModel.email == user.email))
        userCopy = result.scalar_one_or_none()
        if userCopy is None:
            user = UserModel(
                email=user.email,
                hashed_password=hash_password(user.password),
                full_name=user.full_name,
                role=user.role
                )
            session.add(user)
            await session.commit()
            return {"message": "user successfully registered!"}
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User with this email already exists"
        )