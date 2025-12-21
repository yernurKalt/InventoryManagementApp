from datetime import datetime, timezone
from typing import Optional
from fastapi import APIRouter, Depends, HTTPException, status

from app.api.deps import get_current_user, require_admin
from app.dao.category_dao import add_category, delete_category_from_db, get_all_categories, get_category_by_id, get_category_by_name, get_updated_category
from app.models import category
from app.models.user import UserModel
from app.schemas.category import CategoryCreate, CategoryOut, CategoryUpdate


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
async def create_category(category: CategoryCreate, admin_user: UserModel = Depends(require_admin)):
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

@router.patch("/{id}")
async def update_category(id: int, name: Optional[str] = None, description: Optional[str] = None, admin_user: UserModel = Depends(require_admin)):
    category = await get_category_by_name(name)
    if category:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"There is already a category with name {name} and its id {category.id}",
            headers={"WWW-Authenticate": "Bearer"}
        )
    update = CategoryUpdate(name=name, description=description)
    category = await get_updated_category(id, update)
    category = CategoryOut.model_validate(category)
    return category.model_dump()


@router.delete("/{id}")
async def delete_category(id: int, admin_user: UserModel = Depends(require_admin)):
    category = await get_category_by_id(id)
    if category is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Could not find category with id {id}",
            headers={"WWW-Authenticate": "Bearer"}
        )
    await delete_category_from_db(id)
    return {"message": "removed"}