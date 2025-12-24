import math
from typing import Optional
from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy import select
from sqlalchemy.orm import selectinload

from app.api.deps import get_current_user, require_admin
from app.dao.category_dao import CategoryDAO
from app.dao.product_dao import ProductDAO
from app.dao.supplier_dao import SupplierDAO
from app.db.db import async_session_maker
from app.models.product import ProductModel
from app.models.user import UserModel
from app.schemas.product import ProductCreate, ProductOut, ProductUpdate
from app.services.pagination_response import pagination_response
from app.services.product_service import filter_products_by_category_and_supplier, get_active_or_inactive_products, is_low_stock, product_check


router = APIRouter(
    prefix="/products",
    tags=["products"]
)


@router.get("")
async def get_all_products(
    size: int = Query(20, ge=1, le=100),
    page: int = Query(0, ge=0),
    category_id: Optional[int] = None,
    supplier_id: Optional[int] = None,
    name: Optional[str] = None,
    is_active: Optional[bool] = None,
    low_stock: bool = False,
    current_user: UserModel = Depends(get_current_user),
    ):
    products = await ProductDAO.get_all_models(q=name)
    products = filter_products_by_category_and_supplier(products=products, category_id=category_id, supplier_id=supplier_id)
    products = get_active_or_inactive_products(products=products, is_active=is_active)
    products = is_low_stock(products=products, low_stock=low_stock)
    return pagination_response(arr=products, size=size, page=page)

@router.get("/{id}")
async def get_product(id: int, current_user: UserModel = Depends(get_current_user)):
    product = await ProductDAO.get_model_by_id(id=id)
    if product is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Product is not found",
            headers={"WWW-Authenticate": "Bearer"}
        )
    product = ProductOut.model_validate(product)
    return product.model_dump()

@router.post("")
async def add_product(product: ProductCreate, admin_user: UserModel = Depends(require_admin)):
    await product_check(product)
    product = await ProductDAO.add_model(**product.model_dump())
    product = ProductOut.model_validate(await ProductDAO.output_product_addition(product=product))
    return product.model_dump()
    
    

@router.patch("/{id}")
async def update_product(id: int, update: ProductUpdate, admin_user: UserModel = Depends(require_admin)):
    pass

@router.delete("/{id}")
async def delete_product(id: int, admin_user: UserModel = Depends(require_admin)):
    pass