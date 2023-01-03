from megano.core.loading import is_model_registered
from .abstract_models import *

__all__ = []

if not is_model_registered("product", "Product"):
    class Product(AbstractProductClass):
        pass

    __all__.append("Product")

if not is_model_registered("product", "ProductCommercial"):
    class ProductCommercial(AbstractProductCommercialClass):
        pass

    __all__.append("ProductCommercial")
