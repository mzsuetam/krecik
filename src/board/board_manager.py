import time

from board.board import Board
from board.enums import Gatherable, Terrain
from display.board_publisher import BoardPublisher, EventType
from interpreter.krecik_types import logicki
from interpreter.krecik_types.logicki import Logicki
from interpreter.krecik_types.nedostatek import KRECIK_NONE, Nedostatek


class BoardManager:
    def __init__(self, board: Board, board_publisher: BoardPublisher) -> None:
        self.board = board
        self.board_publisher = board_publisher

    # changing position and direction:
    def move_krecik_forward(self, number_of_steps: int) -> Nedostatek:
        for _ in range(number_of_steps):
            is_move_successful = self._make_krecik_move()
            if not is_move_successful:
                break
        return KRECIK_NONE

    def _make_krecik_move(self) -> bool:
        new_pos = self.board.krecik.next_position()
        if not (new_tile := self.board.get_tile(row=new_pos.row, col=new_pos.col)):
            return False
        if not new_tile.can_step_on():
            return False
        self.board.krecik.position = new_pos
        self.board_publisher.notify(EventType.POSITION)
        return True

    def turn_krecik_right(self) -> Nedostatek:
        self.board.krecik.rotate(1)
        self.board_publisher.notify(EventType.ROTATION)
        return KRECIK_NONE

    def turn_krecik_180(self) -> Nedostatek:
        self.board.krecik.rotate(2)
        self.board_publisher.notify(EventType.ROTATION)
        return KRECIK_NONE

    def turn_krecik_left(self) -> Nedostatek:
        self.board.krecik.rotate(3)
        self.board_publisher.notify(EventType.ROTATION)
        return KRECIK_NONE

    # interaction with objects:
    def krecik_pick_up(self) -> Nedostatek:
        tile = self.board.get_krecik_tile()
        is_success = tile.transfer_to(self.board.krecik)
        if is_success:
            self.board_publisher.notify(EventType.PICK)
        return KRECIK_NONE

    def krecik_put(self) -> Nedostatek:
        tile = self.board.get_krecik_tile()
        is_success = self.board.krecik.transfer_to(tile)
        if is_success:
            self.board_publisher.notify(EventType.PUT)
        return KRECIK_NONE

    def krecik_make_mound(self) -> Nedostatek:
        tile = self.board.get_krecik_tile()
        if tile.is_terrain(Terrain.GRASS):
            tile.change_terrain(Terrain.MOUND)
            self.board_publisher.notify(EventType.MAKE_MOUND)
        return KRECIK_NONE

    def krecik_remove_mound(self) -> Nedostatek:
        tile = self.board.get_krecik_tile()
        if tile.is_terrain(Terrain.MOUND):
            tile.change_terrain(Terrain.GRASS)
            self.board_publisher.notify(EventType.REMOVE_MOUND)
        return KRECIK_NONE

    def krecik_hide_in_mound(self) -> Nedostatek:
        tile = self.board.get_krecik_tile()
        krecik = self.board.krecik
        if not krecik.is_in_mound and tile.is_terrain(Terrain.MOUND):
            krecik.is_in_mound = True
            self.board_publisher.notify(EventType.HIDE)
        return KRECIK_NONE

    def krecik_get_out_of_mound(self) -> Nedostatek:
        tile = self.board.get_krecik_tile()
        krecik = self.board.krecik
        if krecik.is_in_mound and tile.is_terrain(Terrain.MOUND):
            krecik.is_in_mound = False
            self.board_publisher.notify(EventType.GET_OUT)
        return KRECIK_NONE

    def is_krecik_on_grass(self) -> Logicki:
        tile = self.board.get_krecik_tile()
        return Logicki(tile.is_terrain(Terrain.GRASS))

    def is_grass_in_front_of_krecik(self) -> Logicki:
        tile = self.board.get_krecik_next_tile()
        if tile is None:
            return logicki.KRECIK_FALSE
        return Logicki(tile.is_terrain(Terrain.GRASS))

    def is_krecik_on_rocks(self) -> Logicki:
        tile = self.board.get_krecik_tile()
        return Logicki(tile.is_terrain(Terrain.ROCKS))

    def is_rocks_in_front_of_krecik(self) -> Logicki:
        tile = self.board.get_krecik_next_tile()
        if tile is None:
            return logicki.KRECIK_TRUE  # out of bound is treated as rocks
        return Logicki(tile.is_terrain(Terrain.ROCKS))

    def is_krecik_on_mound(self) -> Logicki:
        tile = self.board.get_krecik_tile()
        return Logicki(tile.is_terrain(Terrain.MOUND))

    def is_mound_in_front_of_krecik(self) -> Logicki:
        tile = self.board.get_krecik_next_tile()
        if tile is None:
            return logicki.KRECIK_FALSE
        return Logicki(tile.is_terrain(Terrain.MOUND))

    def is_krecik_on_tomato(self) -> Logicki:
        tile = self.board.get_krecik_tile()
        return Logicki(tile.has_gatherable(Gatherable.TOMATO))

    def is_tomato_in_front_of_krecik(self) -> Logicki:
        tile = self.board.get_krecik_next_tile()
        if tile is None:
            return logicki.KRECIK_FALSE
        return Logicki(tile.has_gatherable(Gatherable.TOMATO))

    def is_krecik_on_mushroom(self) -> Logicki:
        tile = self.board.get_krecik_tile()
        return Logicki(tile.has_gatherable(Gatherable.MUSHROOM))

    def is_mushroom_in_front_of_krecik(self) -> Logicki:
        tile = self.board.get_krecik_next_tile()
        if tile is None:
            return logicki.KRECIK_FALSE
        return Logicki(tile.has_gatherable(Gatherable.MUSHROOM))

    # other methods:
    def is_krecik_holding_tomato(self) -> Logicki:
        return Logicki(self.board.krecik.has_gatherable(Gatherable.TOMATO))

    def is_krecik_holding_mushroom(self) -> Logicki:
        return Logicki(self.board.krecik.has_gatherable(Gatherable.MUSHROOM))

    def wait(self, sleep_time: float) -> Nedostatek:
        time.sleep(sleep_time)
        return KRECIK_NONE
