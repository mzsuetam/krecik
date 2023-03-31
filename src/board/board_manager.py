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
            self._make_move()
        self.board_publisher.notify(EventType.POSITION, self.board)

    def _make_move(self) -> None:
        new_pos = self.board.krecik.next_position()
        if not (new_tile := self.board.get(row=new_pos.row, col=new_pos.col)):
            return
        if not new_tile.can_step_on():
            return
        self.board.krecik.position = new_pos

    def turn_right(self) -> None:
        self.board.krecik.rotate(1)
        self.board_publisher.notify(EventType.ROTATION, self.board)

    def turn_left(self) -> None:
        self.board.krecik.rotate(-1)
        self.board_publisher.notify(EventType.ROTATION, self.board)

    def turn_180(self) -> None:
        self.board.krecik.rotate(2)
        self.board_publisher.notify(EventType.ROTATION, self.board)

    def wait(self, sleep_time: KrecikFunctionArgument) -> None:
        self._validate_float(sleep_time)
        time.sleep(sleep_time)

    def pick_up(self) -> None:
        tile = self.board.get_krecik_tile()
        if self.board.krecik.can_pick() and tile.gatherable is not None:
            gatherable = tile.pick()
            self.board.krecik.inventory.append(gatherable)

    def put(self) -> None:
        tile = self.board.get_krecik_tile()
        if tile.gatherable is None:
            gatherable = self.board.krecik.pop_from_inventory()
            tile.gatherable = gatherable

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
