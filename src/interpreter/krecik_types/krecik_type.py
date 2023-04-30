from abc import ABC, abstractmethod
from typing import TYPE_CHECKING

from interpreter.exceptions import KrecikIncompatibleTypesError

if TYPE_CHECKING:
    from typing import Any


class KrecikType(ABC):
    type_name: str

    def __init__(self, value: "Any") -> None:
        self.value = value

    @property
    def value(self) -> "Any":
        return self._value

    @value.setter
    def value(self, value: "Any") -> None:
        self._value = self._parse_value(value) if value is not None else None

    @abstractmethod
    def _parse_value(self, value: str) -> "Any":
        pass

    def __str__(self) -> str:
        return f"{self.type_name}: {self.value}"

    def __repr__(self) -> str:
        return str(self)

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, KrecikType):
            return False
        return all(
            (
                self.value == other.value,
                self.type_name == other.type_name,
            ),
        )

    # unary operators
    def __neg__(self) -> "KrecikType":
        raise KrecikIncompatibleTypesError(
            operand="-",
            type_1=self.type_name,
        )

    def __pos__(self) -> "KrecikType":
        raise KrecikIncompatibleTypesError(
            operand="+",
            type_1=self.type_name,
        )

    def __invert__(self) -> "KrecikType":
        raise KrecikIncompatibleTypesError(
            operand="~",
            type_1=self.type_name,
        )

    # arithmetic operators
    def __add__(self, other: "Any") -> "KrecikType":
        raise KrecikIncompatibleTypesError(
            operand="+",
            type_1=self.type_name,
            type_2=other.type_name,
        )

    def __sub__(self, other: "Any") -> "KrecikType":
        raise KrecikIncompatibleTypesError(
            operand="-",
            type_1=self.type_name,
            type_2=other.type_name,
        )

    def __mul__(self, other: "Any") -> "KrecikType":
        raise KrecikIncompatibleTypesError(
            operand="*",
            type_1=self.type_name,
            type_2=other.type_name,
        )

    def __truediv__(self, other: "Any") -> "KrecikType":
        raise KrecikIncompatibleTypesError(
            operand="/",
            type_1=self.type_name,
            type_2=other.type_name,
        )

    # comparison operators
    def __gt__(self, other: "Any") -> "KrecikType":
        raise KrecikIncompatibleTypesError(
            operand="wetsi",
            type_1=self.type_name,
            type_2=other.type_name,
        )

    def __lt__(self, other: "Any") -> "KrecikType":
        raise KrecikIncompatibleTypesError(
            operand="mensi",
            type_1=self.type_name,
            type_2=other.type_name,
        )

    def is_equal(self, other: "Any") -> "KrecikType":
        raise KrecikIncompatibleTypesError(
            operand="je",
            type_1=self.type_name,
            type_2=other.type_name,
        )

    def is_not_equal(self, other: "Any") -> "KrecikType":
        raise KrecikIncompatibleTypesError(
            operand="neje",
            type_1=self.type_name,
            type_2=other.type_name,
        )

    # logical operators
    def __and__(self, other: "Any") -> "KrecikType":
        raise KrecikIncompatibleTypesError(
            operand="oba",
            type_1=self.type_name,
            type_2=other.type_name,
        )

    def __or__(self, other: "Any") -> "KrecikType":
        raise KrecikIncompatibleTypesError(
            operand="nebo",
            type_1=self.type_name,
            type_2=other.type_name,
        )
