from interpreter.krecik_types.krecik_type import KrecikType


class Nedostatek(KrecikType):
    type_name = "nedostatek"

    def _parse_value(self, value: str) -> None:
        return None


KRECIK_NONE = Nedostatek(None)
