from megano.core.loading import is_model_registered
from .abstract_models import *


__all__ = []

if not is_model_registered('catalog', 'Category'):
    class Category(AbstractCategory):
        pass

    __all__.append("Category")

if not is_model_registered('catalog', 'CategoryCommercial'):
    class CategoryCommercial(AbstractCommercialCategory):
        pass

    __all__.append("CategoryCommercial")



