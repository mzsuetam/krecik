from typing import TYPE_CHECKING

from interpreter.exceptions import (
    KrecikValueError,
    KrecikIncompatibleTypesError,
    KrecikZeroDivisionError,
)
from interpreter.krecik_types.krecik_type import KrecikType
from interpreter.krecik_types.logicki import Logicki

if TYPE_CHECKING:
    from typing import Any


class Cislo(KrecikType):
    type_name = "cislo"

    def _parse_value(self, value: "Any") -> float:
        if isinstance(value, float):
            return value
        if isinstance(value, str):
            return float(value)
        raise KrecikValueError(type_name=self.type_name, value=value)

    # unary operators
    def __neg__(self) -> "Cislo":
        return Cislo(-self.value)

    def __pos__(self) -> "Cislo":
        return Cislo(+self.value)

    # arithmetic operators
    def __add__(self, other: "Any") -> "Cislo":
        if isinstance(other, Cislo):
            return Cislo(self.value + other.value)
        raise KrecikIncompatibleTypesError(
            operand="+",
            type_1=self.type_name,
            type_2=other.type_name,
        )

    def __sub__(self, other: "Any") -> "Cislo":
        if isinstance(other, Cislo):
            return Cislo(self.value - other.value)
        raise KrecikIncompatibleTypesError(
            operand="-",
            type_1=self.type_name,
            type_2=other.type_name,
        )

    def __mul__(self, other: "Any") -> "Cislo":
        if isinstance(other, Cislo):
            return Cislo(self.value * other.value)
        raise KrecikIncompatibleTypesError(
            operand="*",
            type_1=self.type_name,
            type_2=other.type_name,
        )

    def __truediv__(self, other: "Any") -> "Cislo":
        try:
            if isinstance(other, Cislo):
                return Cislo(self.value / other.value)
        except ZeroDivisionError:
            raise KrecikZeroDivisionError()
        raise KrecikIncompatibleTypesError(
            operand="/",
            type_1=self.type_name,
            type_2=other.type_name,
        )

    # comparison operators
    def __gt__(self, other: "Any") -> "Logicki":
        if isinstance(other, Cislo):
            return Logicki(self.value > other.value)
        raise KrecikIncompatibleTypesError(
            operand="wetsi",
            type_1=self.type_name,
            type_2=other.type_name,
        )

    def __lt__(self, other: "Any") -> "Logicki":
        if isinstance(other, Cislo):
            return Logicki(self.value < other.value)
        raise KrecikIncompatibleTypesError(
            operand="mensi",
            type_1=self.type_name,
            type_2=other.type_name,
        )

    def is_equal(self, other: "Any") -> "Logicki":
        if isinstance(other, Cislo):
            return Logicki(self.value == other.value)
        raise KrecikIncompatibleTypesError(
            operand="je",
            type_1=self.type_name,
            type_2=other.type_name,
        )

    def is_not_equal(self, other: "Any") -> "Logicki":
        if isinstance(other, Cislo):
            return Logicki(self.value != other.value)
        raise KrecikIncompatibleTypesError(
            operand="neje",
            type_1=self.type_name,
            type_2=other.type_name,
        )
