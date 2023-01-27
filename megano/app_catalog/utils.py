from interfaces.data_access_objects.abstract_dao import AbstractModelDAO
from interfaces.data_transfer_objects.abstract_dto import AbstractEntity
from dataclasses import dataclass
from megano.core.loading import get_model


Category = get_model('catalog', 'Category')

@dataclass
class CategoryDTO(AbstractEntity):
    name: str
    description: str
    image: str
    slug: str
    is_public: bool


class CategoryDAO(AbstractModelDAO):
    class Meta:
        entity = CategoryDTO
        model = Category