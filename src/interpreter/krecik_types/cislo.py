from typing import Any

from interpreter.exceptions import KrecikValueError, KrecikIncompatibleTypes
from interpreter.krecik_types.krecik_type import KrecikType
from interpreter.krecik_types.logicki import Logicki


class Cislo(KrecikType):
    type_name = "cislo"

    def _parse_value(self, value: Any) -> float:
        if isinstance(value, float):
            return value
        if isinstance(value, str):
            return float(value)
        raise KrecikValueError(type_name=self.type_name, value=value)

    def __add__(self, other: Any) -> KrecikType:
        if isinstance(other, self.__class__):
            return Cislo(self.value + other.value)
        raise KrecikIncompatibleTypes(
            operand_type="+", type_1=self.type_name, type_2=other.type_name
        )

    def __sub__(self, other: Any) -> KrecikType:
        if isinstance(other, self.__class__):
            return Cislo(self.value - other.value)
        raise KrecikIncompatibleTypes(
            operand_type="-", type_1=self.type_name, type_2=other.type_name
        )

    def __mul__(self, other: Any) -> KrecikType:
        if isinstance(other, self.__class__):
            return Cislo(self.value * other.value)
        raise KrecikIncompatibleTypes(
            operand_type="*", type_1=self.type_name, type_2=other.type_name
        )

    def __truediv__(self, other: Any) -> KrecikType:
        if isinstance(other, self.__class__):
            return Cislo(self.value // other.value)
        raise KrecikIncompatibleTypes(
            operand_type="/", type_1=self.type_name, type_2=other.type_name
        )

    def __neg__(self, other: Any) -> KrecikType:
        return Cislo(-self.value)

    def __gt__(self, other: Any) -> Any:
        if isinstance(other, self.__class__):
            return Logicki(self.value > other.value)
        raise KrecikIncompatibleTypes(
            operand_type="wetsi", type_1=self.type_name, type_2=other.type_name
        )

    def __lt__(self, other: Any) -> Any:
        if isinstance(other, self.__class__):
            return Logicki(self.value < other.value)
        raise KrecikIncompatibleTypes(
            operand_type="mensi", type_1=self.type_name, type_2=other.type_name
        )

    def __eq__(self, other: Any) -> Any:
        if isinstance(other, self.__class__):
            return Logicki(self.value == other.value)
        raise KrecikIncompatibleTypes(
            operand_type="je", type_1=self.type_name, type_2=other.type_name
        )

    def __ne__(self, other: Any) -> Any:
        if isinstance(other, self.__class__):
            return Logicki(self.value != other.value)
        raise KrecikIncompatibleTypes(
            operand_type="neje", type_1=self.type_name, type_2=other.type_name
        )
