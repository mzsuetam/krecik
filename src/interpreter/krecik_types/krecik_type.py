from abc import ABC, abstractmethod
from typing import Any


class KrecikType(ABC):
    type_name: str

    def __init__(self, value: Any) -> None:
        self.value = value

    @property
    def value(self) -> Any:
        return self._value

    @value.setter
    def value(self, value: Any) -> None:
        self._value = self._parse_value(value) if value is not None else None

    @abstractmethod
    def _parse_value(self, value: str) -> Any:
        pass

    def __str__(self) -> str:
        return f"{self.type_name}: {self.value}"

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, KrecikType):
            return False
        return all(
            (
                self.value == other.value,
                self.type_name == other.type_name,
            ),
        )
