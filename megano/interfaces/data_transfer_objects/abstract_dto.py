from dataclasses import dataclass, asdict, astuple
import abc

@dataclass
class AbstractEntity(abc.ABC):
    """Data transfer object abtract class."""
    id: int
    
    def get_as_dict(self):
        return asdict(self)
    
    def get_as_list(self):
        return list(astuple(self))

    def get_as_set(self):
        return set(astuple(self))

    def get_as_tuple(self):
        return astuple(self)
