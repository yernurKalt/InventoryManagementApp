from datetime import datetime
from typing import Optional
from fastapi import HTTPException, status
from sqlalchemy import delete, select
from app.dao.base import BaseDAO
from app.db.db import async_session_maker
from app.models.category import CategoryModel
from app.schemas.category import CategoryCreate, CategoryUpdate


class CategoryDAO(BaseDAO):
    model = CategoryModel
    updt = CategoryUpdate