import time
from typing import TypeAlias

from board.board import Board
from display.board_publisher import BoardPublisher, EventType
from interpreter.exceptions import IncorrectArgumentTypeError

KrecikFunctionArgument: TypeAlias = int | float | bool


class BoardManager:

    def __init__(self, board: Board, board_publisher: BoardPublisher) -> None:
        self.board = board
        self.board_publisher = board_publisher

    def move_forward(self, number_of_steps: KrecikFunctionArgument) -> None:
        number_of_steps = int(number_of_steps)  # FIXME
        self._validate_int(number_of_steps)
        for _ in range(number_of_steps):
            is_move_successful = self._make_move()
            if not is_move_successful:
                return
        self.board_publisher.notify(EventType.POSITION)

    def _make_move(self) -> bool:
        new_pos = self.board.krecik.next_position()
        if not (new_tile := self.board.get(row=new_pos.row, col=new_pos.col)):
            return False
        if not new_tile.can_step_on():
            return False
        self.board.krecik.position = new_pos
        return True

    def turn_right(self) -> None:
        self.board.krecik.rotate(1)
        self.board_publisher.notify(EventType.ROTATION)

    def turn_180(self) -> None:
        self.board.krecik.rotate(2)
        self.board_publisher.notify(EventType.ROTATION)

    def turn_left(self) -> None:
        self.board.krecik.rotate(3)
        self.board_publisher.notify(EventType.ROTATION)

    def wait(self, sleep_time: KrecikFunctionArgument) -> None:
        self._validate_float(sleep_time)
        time.sleep(sleep_time)

    def pick_up(self) -> None:
        tile = self.board.get_krecik_tile()
        if self.board.krecik.can_pick():
            if gatherable := tile.pick():
                self.board.krecik.inventory.append(gatherable)
                self.board_publisher.notify(EventType.PICK)

    def put(self) -> None:
        tile = self.board.get_krecik_tile()
        if tile.gatherable is None:
            if gatherable := self.board.krecik.pop_from_inventory():
                tile.gatherable = gatherable
                self.board_publisher.notify(EventType.PUT)

    @staticmethod
    def _validate_int(arg: KrecikFunctionArgument) -> None:
        if isinstance(arg, int):
            return
        raise IncorrectArgumentTypeError()

    @staticmethod
    def _validate_float(arg: KrecikFunctionArgument) -> None:
        if isinstance(arg, float):
            return
        raise IncorrectArgumentTypeError()

    @staticmethod
    def _validate_bool(arg: KrecikFunctionArgument) -> None:
        if isinstance(arg, bool):
            return
        raise IncorrectArgumentTypeError()
