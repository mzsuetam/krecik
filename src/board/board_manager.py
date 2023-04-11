import time
from typing import TypeAlias

from board.board import Board
from board.enums import Gatherable, Terrain
from display.board_publisher import BoardPublisher, EventType
from interpreter.exceptions import IncorrectArgumentTypeError

KrecikFunctionArgument: TypeAlias = int | float | bool


class BoardManager:

    def __init__(self, board: Board, board_publisher: BoardPublisher) -> None:
        self.board = board
        self.board_publisher = board_publisher

    # changing position and direction:
    def move_krecik_forward(self, number_of_steps: KrecikFunctionArgument) -> None:
        number_of_steps = int(number_of_steps)  # FIXME
        self._validate_int(number_of_steps)
        for _ in range(number_of_steps):
            is_move_successful = self._make_krecik_move()
            if not is_move_successful:
                return

    def _make_krecik_move(self) -> bool:
        new_pos = self.board.krecik.next_position()
        if not (new_tile := self.board.get_tile(row=new_pos.row, col=new_pos.col)):
            return False
        if not new_tile.can_step_on():
            return False
        self.board.krecik.position = new_pos
        self.board_publisher.notify(EventType.POSITION)
        return True

    def turn_krecik_right(self) -> None:
        self.board.krecik.rotate(1)
        self.board_publisher.notify(EventType.ROTATION)

    def turn_krecik_180(self) -> None:
        self.board.krecik.rotate(2)
        self.board_publisher.notify(EventType.ROTATION)

    def turn_krecik_left(self) -> None:
        self.board.krecik.rotate(3)
        self.board_publisher.notify(EventType.ROTATION)

    # interaction with objects:
    def krecik_pick_up(self) -> None:
        tile = self.board.get_krecik_tile()
        is_success = tile.transfer_to(self.board.krecik)
        if is_success:
            self.board_publisher.notify(EventType.PICK)

    def krecik_put(self) -> None:
        tile = self.board.get_krecik_tile()
        is_success = self.board.krecik.transfer_to(tile)
        if is_success:
            self.board_publisher.notify(EventType.PUT)

    def krecik_make_mound(self) -> None:
        tile = self.board.get_krecik_tile()
        if tile.is_terrain(Terrain.GRASS):
            tile.change_terrain(Terrain.MOUND)
            self.board_publisher.notify(EventType.MAKE_MOUND)

    def krecik_remove_mound(self) -> None:
        tile = self.board.get_krecik_tile()
        if tile.is_terrain(Terrain.MOUND):
            tile.change_terrain(Terrain.GRASS)
            self.board_publisher.notify(EventType.REMOVE_MOUND)

    def krecik_hide_in_mound(self) -> None:
        tile = self.board.get_krecik_tile()
        krecik = self.board.krecik
        if not krecik.is_in_mound and tile.is_terrain(Terrain.MOUND):
            krecik.is_in_mound = True
            self.board_publisher.notify(EventType.HIDE)

    def krecik_get_out_of_mound(self) -> None:
        tile = self.board.get_krecik_tile()
        krecik = self.board.krecik
        if krecik.is_in_mound and tile.is_terrain(Terrain.MOUND):
            krecik.is_in_mound = False
            self.board_publisher.notify(EventType.GET_OUT)

    def is_krecik_on_grass(self) -> bool:
        tile = self.board.get_krecik_tile()
        return tile.is_terrain(Terrain.GRASS)

    def is_grass_in_front_of_krecik(self) -> bool:
        tile = self.board.get_krecik_next_tile()
        if tile is None:
            return False
        return tile.is_terrain(Terrain.GRASS)

    def is_krecik_on_rocks(self) -> bool:
        tile = self.board.get_krecik_tile()
        return tile.is_terrain(Terrain.ROCKS)

    def is_rocks_in_front_of_krecik(self) -> bool:
        tile = self.board.get_krecik_next_tile()
        if tile is None:
            return True  # out of bound is treated as rocks
        return tile.is_terrain(Terrain.ROCKS)

    def is_krecik_on_mound(self) -> bool:
        tile = self.board.get_krecik_tile()
        return tile.is_terrain(Terrain.MOUND)

    def is_mound_in_front_of_krecik(self) -> bool:
        tile = self.board.get_krecik_next_tile()
        if tile is None:
            return False
        return tile.is_terrain(Terrain.MOUND)

    def is_krecik_on_tomato(self) -> bool:
        tile = self.board.get_krecik_tile()
        return tile.has_gatherable(Gatherable.TOMATO)

    def is_tomato_in_front_of_krecik(self) -> bool:
        tile = self.board.get_krecik_next_tile()
        if tile is None:
            return False
        return tile.has_gatherable(Gatherable.TOMATO)

    def is_krecik_on_mushroom(self) -> bool:
        tile = self.board.get_krecik_tile()
        return tile.has_gatherable(Gatherable.MUSHROOM)

    def is_mushroom_in_front_of_krecik(self) -> bool:
        tile = self.board.get_krecik_next_tile()
        if tile is None:
            return False
        return tile.has_gatherable(Gatherable.MUSHROOM)

    # other methods:
    def is_krecik_holding_tomato(self) -> bool:
        return self.board.krecik.has_gatherable(Gatherable.TOMATO)

    def is_krecik_holding_mushroom(self) -> bool:
        return self.board.krecik.has_gatherable(Gatherable.MUSHROOM)

    def wait(self, sleep_time: KrecikFunctionArgument) -> None:
        self._validate_float(sleep_time)
        time.sleep(sleep_time)

    # arguments validation
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
