from datetime import datetime, timedelta, timezone
from typing import Annotated

import jwt
from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jwt.exceptions import InvalidTokenError
from pwdlib import PasswordHash
from pydantic import BaseModel

from app.api.deps import get_current_user, require_admin
from app.models.user import UserModel
from app.routers.auth import router as login_router
from app.routers.users import router as users_router
from app.routers.categories import router as categories_router
from app.routers.suppliers import router as suppliers_router
from app.schemas.user import UserOut


app = FastAPI()

app.include_router(login_router)
app.include_router(users_router)
app.include_router(categories_router)
app.include_router(suppliers_router)