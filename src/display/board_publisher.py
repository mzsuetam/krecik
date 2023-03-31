from enum import Enum

from board.board import Board
from display.base_display import BaseDisplay


class EventType(Enum):
    POSITION = 0
    ROTATION = 1
    PICK = 2
    PUT = 3


class BoardPublisher:

    def __init__(self) -> None:
        self.displays = []
        self._event_type_to_method_map = {
            EventType.POSITION: self.notify_position,
            EventType.ROTATION: self.notify_rotation,
        }

    def subscribe(self, display: BaseDisplay) -> None:
        self.displays.append(display)

    def unsubscribe(self, display: BaseDisplay) -> None:
        self.displays.remove(display)

    def notify(self, event_type: EventType, board: Board) -> None:
        method = self._event_type_to_method_map.get(event_type)
        for display in self.displays:
            method(display, board)

    @staticmethod
    def notify_position(display: BaseDisplay, board: Board) -> None:
        display.update_krecik_position(board.krecik)

    @staticmethod
    def notify_rotation(display: BaseDisplay, board: Board) -> None:
        display.update_krecik_rotation(board.krecik)
