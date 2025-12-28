from datetime import datetime, timezone
import math
from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, Query, status

from app.api.deps import get_current_user, require_admin
from app.dao.category_dao import CategoryDAO
from app.models import category
from app.models.user import UserModel
from app.schemas.category import CategoryCreate, CategoryOut, CategoryOutWithProducts, CategoryUpdate
from app.schemas.pagination import Page, PageMeta
from app.services.pagination_response import pagination_response


router = APIRouter(
    prefix="/categories",
    tags=["categories"]
)


@router.get("")
async def get_categories(
    size: int = Query(20, ge=1, le=100),
    page: int = Query(0, ge = 0),
    name: Optional[str] = None,
    current_user: UserModel = Depends(get_current_user),
    ):
    #pass
    items = await CategoryDAO.get_all_models(q=name)
    result = []
    for item in items:
        result.append(CategoryOutWithProducts.model_validate(item))
    return pagination_response(arr=result, size=size, page=page)

@router.get("/{id}")
async def get_category_by_id(id: int, current_user: UserModel = Depends(get_current_user)):
    category = await CategoryDAO.get_model_by_id(id)
    if category is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Could not find category with id {id}",
            headers={"WWW-Authenticate": "Bearer"}
        )
    category = CategoryOutWithProducts.model_validate(category)
    return category.model_dump()

 
@router.post("")
async def create_category(category: CategoryCreate, admin_user: UserModel = Depends(require_admin)):
    old_category = await CategoryDAO.get_model_by_name(category.name)
    if old_category:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Category already exists",
            headers={"WWW-Authenticate": "Bearer"}
        )
    result = await CategoryDAO.add_model(**category.model_dump())
    category = CategoryOut.model_validate(result)
    return category.model_dump()

@router.patch("/{id}")
async def update_category(id: int, update: CategoryUpdate, admin_user: UserModel = Depends(require_admin)):
    if update.name:
        category = await CategoryDAO.get_model_by_name(update.name)
        if category:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail=f"There is already a category with name {update.name} and its id {category.id}",
                headers={"WWW-Authenticate": "Bearer"}
            )
    category = await CategoryDAO.get_updated_model(id, **update.model_dump())
    category = CategoryOutWithProducts.model_validate(category)
    return category.model_dump()


@router.delete("/{id}")
async def delete_category(id: int, admin_user: UserModel = Depends(require_admin)):
    category = await CategoryDAO.get_model_by_id(id)
    if category is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Could not find category with id {id}",
            headers={"WWW-Authenticate": "Bearer"}
        )
    await CategoryDAO.delete_model_from_db(id)
    return {"message": "removed"}