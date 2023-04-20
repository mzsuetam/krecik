from typing import Any

from interpreter.exceptions import KrecikValueError
from interpreter.krecik_types.krecik_type import KrecikType


class Logicki(KrecikType):
    type_name = "logicki"
    true_values = {"pravda", "true", "1"}
    false_values = {"nepravda", "false", "0"}

    def _parse_value(self, value: Any) -> bool:
        if isinstance(value, bool):
            return value
        if isinstance(value, str):
            if value in self.true_values:
                return True
            if value in self.false_values:
                return False
        raise KrecikValueError(type_name=self.type_name, value=value)

    def __invert__(self) -> KrecikType:
        return Logicki(not self.value)

    def __bool__(self) -> bool:
        return self.value


KRECIK_TRUE = Logicki(True)
KRECIK_FALSE = Logicki(False)
