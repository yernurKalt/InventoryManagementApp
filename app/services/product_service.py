from typing import Optional

from fastapi import HTTPException, status
from app.dao.category_dao import CategoryDAO
from app.dao.product_dao import ProductDAO
from app.dao.supplier_dao import SupplierDAO
from app.models.product import ProductModel
from app.schemas.product import ProductCreate


def filter_products_by_category_and_supplier(products: list[ProductModel], category_id: Optional[int], supplier_id: Optional[int]):
    response = products
    if category_id and supplier_id:
        response = []
        for product in products:
            if product.category_id == category_id and product.supplier_id == supplier_id:
                response.append(product)
    elif category_id and (supplier_id is None):
        response = []
        for product in products:
            if category_id == product.category_id:
                response.append(product)
    elif category_id is None and supplier_id:
        response = []
        for product in products:
            if supplier_id == product.supplier_id:
                response.append(product)
    return response

def get_active_or_inactive_products(products: list[ProductModel], is_active: bool = None):
    if is_active is None:
        return products
    if is_active:
        result = []
        for product in products:
            if product.is_active:
                result.append(product)
    else:
        result = []
        for product in products:
            if not product.is_active:
                result.append(product)
    return result

def is_low_stock(products: list[ProductModel], low_stock: bool):
    if low_stock:
        result = []
        for product in products:
            if product.current_stock <= product.reorder_level:
                result.append(product)
        return result
        
    return products

async def product_check(product: ProductCreate):
    category = await CategoryDAO.get_model_by_id(product.category_id)
    if category is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Category with id {product.category_id} is not found",
            headers={"WWW-Authenticate": "Bearer"}
        )
    supplier = await SupplierDAO.get_model_by_id(product.supplier_id)
    if supplier is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Supplier with id {product.supplier_id} is not found",
            headers={"WWW-Authenticate": "Bearer"}
        )
    old_product = await ProductDAO.get_model_by_name(product.name) or await ProductDAO.find_product_by_sku(sku=product.sku)
    if old_product:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Product with that already exists",
            headers={"WWW-Authenticate": "Bearer"}
        )