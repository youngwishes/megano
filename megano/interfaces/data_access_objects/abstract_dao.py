import abc
from typing import Iterable, List
from ..data_transfer_objects.abstract_dto import AbstractEntity


class AbstractModelDAO(abc.ABC):
    """Data access object abstract class."""
    def __init__(self) -> None:
        self._meta = self.Meta

    def _orm_to_entity(self) -> Iterable:
        for model_instance in self._meta.model.objects.all():
            data = model_instance.__dict__
            data.pop('_state')
            yield self._meta.entity(**data)

    def fetch_all(self) -> List:
        return list(entity for entity in self._orm_to_entity())

    def update(self, *args, many=False, **kwargs) -> None:
        pass
    
    def delete(self, *args, many=False, **kwargs) -> None:
        pass
    
    def create(self, *args, many=False, **kwargs) -> None:
        pass

    def count(self) -> int:
        return self._meta.model.objects.count()

    def __getattr__(self, attribute):
        if attribute in self._meta.methods:
            return getattr(self.__dict__[attribute], attribute)

    class Meta:
        entity = AbstractEntity
        methods = ["fetch_all", "update", "delete", "create", "count"]
        model = None
