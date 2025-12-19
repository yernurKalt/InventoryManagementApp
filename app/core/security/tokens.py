from datetime import datetime, timedelta, timezone
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from typing import Annotated

import jwt
from jwt.exceptions import InvalidTokenError
from pydantic import computed_field
from pydantic_settings import BaseSettings, SettingsConfigDict
from sqlalchemy import select
from sqlalchemy.orm import query
from app.db.config import settings
from app.db.db import async_session_maker
from app.models.user import UserModel
from app.schemas.auth import TokenPayload


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")

def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, settings.KEY, settings.ALGORITHM)
    return encoded_jwt

async def decode_and_validate_token(token: Annotated[str, Depends(oauth2_scheme)]):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"}
    )
    try:
        payload = jwt.decode(token, settings.KEY, algorithms=[settings.ALGORITHM])
        user_id = payload.get("sub")
        user_role = payload.get("role")
        if user_id is None or user_role is None: 
            raise credentials_exception
        token_data = TokenPayload(sub=int(payload.get("sub")), role=payload.get("role"))
        return token_data
    except InvalidTokenError:
        raise credentials_exception