from enum import Enum, auto

from display.base_display import BaseDisplay


class EventType(Enum):
    POSITION = auto()
    ROTATION = auto()
    PICK = auto()
    PUT = auto()
    MAKE_MOUND = auto()
    REMOVE_MOUND = auto()
    HIDE = auto()
    GET_OUT = auto()


class BoardPublisher:
    def __init__(self) -> None:
        self.displays: list[BaseDisplay] = []
        self._event_type_to_method_map = {
            EventType.POSITION: self.notify_position,
            EventType.ROTATION: self.notify_rotation,
        }

    def subscribe(self, display: BaseDisplay) -> None:
        self.displays.append(display)

    def unsubscribe(self, display: BaseDisplay) -> None:
        self.displays.remove(display)

    def notify(self, event_type: EventType) -> None:
        method = self._event_type_to_method_map.get(event_type)
        if method is None:
            raise NotImplementedError()
        for display in self.displays:
            method(display)

    @staticmethod
    def notify_position(display: BaseDisplay) -> None:
        display.update_krecik_position()

    @staticmethod
    def notify_rotation(display: BaseDisplay) -> None:
        display.update_krecik_rotation()
