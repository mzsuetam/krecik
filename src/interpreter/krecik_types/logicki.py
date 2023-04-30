from typing import TYPE_CHECKING

from interpreter.exceptions import KrecikIncompatibleTypesError, KrecikValueError
from interpreter.krecik_types.krecik_type import KrecikType

if TYPE_CHECKING:
    from typing import Any


class Logicki(KrecikType):
    type_name = "logicki"
    true_values = {"true"}
    false_values = {"false"}

    def _parse_value(self, value: "Any") -> bool:
        if isinstance(value, bool):
            return value
        if isinstance(value, str):
            if value in self.true_values:
                return True
            if value in self.false_values:
                return False
        raise KrecikValueError(type_name=self.type_name, value=value)

    # unary operators
    def __invert__(self) -> "Logicki":
        return Logicki(not self.value)

    # comparison operators
    def is_equal(self, other: "Any") -> "Logicki":
        if isinstance(other, Logicki):
            return Logicki(self.value is other.value)
        raise KrecikIncompatibleTypesError(
            operand="==",
            type_1=self.type_name,
            type_2=other.type_name,
        )

    def is_not_equal(self, other: "Any") -> "Logicki":
        if isinstance(other, Logicki):
            return Logicki(self.value is not other.value)
        raise KrecikIncompatibleTypesError(
            operand="!=",
            type_1=self.type_name,
            type_2=other.type_name,
        )

    # logical operators
    def __and__(self, other: "Any") -> "Logicki":
        if isinstance(other, Logicki):
            return Logicki(self.value and other.value)
        raise KrecikIncompatibleTypesError(
            operand="and",
            type_1=self.type_name,
            type_2=other.type_name,
        )

    def __or__(self, other: "Any") -> "Logicki":
        if isinstance(other, Logicki):
            return Logicki(self.value or other.value)
        raise KrecikIncompatibleTypesError(
            operand="or",
            type_1=self.type_name,
            type_2=other.type_name,
        )


KRECIK_TRUE = Logicki(True)
KRECIK_FALSE = Logicki(False)
