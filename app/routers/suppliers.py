import math
from typing import Optional
from fastapi import APIRouter, Depends, HTTPException, Query, status

from app.api.deps import get_current_user, require_admin
from app.dao.supplier_dao import SupplierDAO
from app.models.user import UserModel
from app.schemas.pagination import Page, PageMeta
from app.schemas.supplier import SupplierCreate, SupplierOut, SupplierOutWithProducts, SupplierUpdate
from app.services.pagination_response import pagination_response


router = APIRouter(
    prefix="/suppliers",
    tags=['suppliers'],
)
 

@router.get("")
async def get_all_suppliers(
    size: int = Query(20, ge=1, le=100),
    page: int = Query(0, ge = 0),
    name: Optional[str] = None,
    current_user: UserModel = Depends(get_current_user),
    ):
    items = await SupplierDAO.get_all_models(q=name)
    result = []
    for item in items:
        result.append(SupplierOutWithProducts.model_validate(item))
    return pagination_response(arr=result, size=size, page=page)

@router.get("/{id}")
async def get_supplier_by_id(id: int, current_user: UserModel = Depends(get_current_user)):
    supplier = await SupplierDAO.get_model_by_id(id)
    if supplier is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Could not find supplier with id {id}",
            headers={"WWW-Authenticate": "Bearer"}
        )
    supplier = SupplierOut.model_validate(supplier)
    return supplier.model_dump()

@router.post("")
async def create_supplier(supplier: SupplierCreate, admin_user: UserModel = Depends(require_admin)):
    old_supplier = await SupplierDAO.get_model_by_name(supplier.name)
    if old_supplier:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"Supplier with name {supplier.name} already exists",
            headers={"WWW-Authenticate": "Bearer"}
        )
    result = await SupplierDAO.add_model(**supplier.model_dump())
    supplier = SupplierOut.model_validate(result)
    return supplier.model_dump()
 
@router.patch("/{id}")
async def update_supplier(id: int, update: SupplierUpdate, admin_user: UserModel = Depends(require_admin)):
    if update.name:
        supplier = await SupplierDAO.get_model_by_name(update.name)
        if supplier:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail=f"Supplier with name {update.name} exists and its id {supplier.id}",
                headers={"WWW-Authenticate": "Bearer"}
            )
    supplier = await SupplierDAO.get_updated_model(id, **update.model_dump())
    supplier = SupplierOut.model_validate(supplier)
    return supplier.model_dump()


@router.delete("/{id}")
async def delete_supplier(id: int, admin_user: UserModel = Depends(require_admin)):
    supplier = await SupplierDAO.get_model_by_id(id)
    if supplier is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Cannot delete. Supplier is not found",
            headers={"WWW-Authenticate": "Bearer"}
        )
    await SupplierDAO.delete_model_from_db(id)
    return {"message": "deleted"}