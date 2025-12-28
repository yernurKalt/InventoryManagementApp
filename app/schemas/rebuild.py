from app.schemas.category import CategoryOutWithProducts
from app.schemas.product import ProductOut, ProductinCategoryAndSupplier
from app.schemas.supplier import SupplierOutWithProducts


ProductOut.model_rebuild()
CategoryOutWithProducts.model_rebuild()
SupplierOutWithProducts.model_rebuild()

