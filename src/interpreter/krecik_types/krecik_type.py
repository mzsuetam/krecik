from abc import ABC, abstractmethod
from typing import Any


class KrecikType(ABC):

    type_name: str

    def __init__(self, value: Any) -> None:
        self.value = self._parse_value(value)

    @abstractmethod
    def _parse_value(self, value: str) -> Any:
        pass

    def __str__(self) -> str:
        return f"{self.type_name} {self.value}"
