from typing import Any

from interpreter.exceptions import KrecikValueError
from interpreter.krecik_types.krecik_type import KrecikType


class Cely(KrecikType):
    type_name = "cely"

    def _parse_value(self, value: Any) -> int:
        if isinstance(value, int):
            return value
        if isinstance(value, str):
            return int(value)
        raise KrecikValueError(type_name=self.type_name, value=value)
