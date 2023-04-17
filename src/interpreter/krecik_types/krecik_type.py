from abc import ABC, abstractmethod
from typing import Any


class KrecikType(ABC):

    type_name: str
    value = None
    name = None

    def __init__(self, value: Any, name = None) -> None:
        if value:
            self.value = self._parse_value(value)
        if name:
            self.name = name

    @abstractmethod
    def _parse_value(self, value: str) -> Any:
        pass

    def __str__(self) -> str:
        return f"{self.type_name} {self.name} = {self.value}"
