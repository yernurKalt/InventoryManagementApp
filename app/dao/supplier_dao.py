from app.dao.base import BaseDAO
from app.models.supplier import SupplierModel
from app.schemas.supplier import SupplierUpdate


class SupplierDAO(BaseDAO):
    model = SupplierModel
    updt = SupplierUpdate