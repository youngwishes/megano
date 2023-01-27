import abc

__all__ = ['Service']


class Service(abc.ABC):

    @abc.abstractmethod
    def execute(self, *args, **kwargs):
        pass
