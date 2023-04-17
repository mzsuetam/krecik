from abc import ABC, abstractmethod
from typing import Any


class KrecikType(ABC):

    type_name: str

    def __init__(self, value: Any, name: str | None = None) -> None:
        self.value = self._parse_value(value) if value is not None else None
        self.name = name

    @abstractmethod
    def _parse_value(self, value: str) -> Any:
        pass

    def __str__(self) -> str:
        return f"{self.type_name} {self.name} = {self.value}"
