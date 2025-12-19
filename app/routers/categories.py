from typing import Optional
from fastapi import APIRouter, Depends, HTTPException, status

from app.api.deps import get_current_user, require_admin
from app.dao.category_dao import add_category, get_all_categories, get_category_by_name
from app.models.user import UserModel
from app.schemas.category import CategoryCreate, CategoryOut


router = APIRouter(
    prefix="/categories",
    tags=["categories"]
)


@router.get("")
async def get_categories(current_user: UserModel = Depends(get_current_user)):
    categories = await get_all_categories()
    if categories:
        return categories
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="No categories were found",
        headers={"WWW-Authenticate": "Bearer"}
    )

@router.post("")
async def create_category(category: CategoryCreate, current_user: UserModel = Depends(require_admin)):
    old_category = await get_category_by_name(category.name)
    if old_category:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Category already exists",
            headers={"WWW-Authenticate": "Bearer"}
        )
    result = await add_category(**category.model_dump())
    category = CategoryOut.model_validate(result)
    return category.model_dump()