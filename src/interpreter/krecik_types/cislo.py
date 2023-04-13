from typing import Any

from interpreter.exceptions import KrecikValueError
from interpreter.krecik_types.krecik_type import KrecikType


class Cislo(KrecikType):

    type_name = "cislo"

    def _parse_value(self, value: Any) -> float:
        if isinstance(value, float):
            return value
        if isinstance(value, str):
            return float(value)
        raise KrecikValueError(type_name=self.type_name, value=value)
