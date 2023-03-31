from random import randrange

from board.board import Board
from board.krecik import Position
from board.tile import TileType


def plains(width: int, height: int) -> Board:
    return Board([[TileType.GRASS] * width] * height)


def jebus_cross() -> Board:
    return Board(
        [
            [TileType.ROCKS, TileType.ROCKS, TileType.GRASS, TileType.ROCKS, TileType.ROCKS],
            [TileType.ROCKS, TileType.ROCKS, TileType.GRASS, TileType.ROCKS, TileType.ROCKS],
            [TileType.GRASS, TileType.GRASS, TileType.MOUND, TileType.GRASS, TileType.GRASS],
            [TileType.ROCKS, TileType.ROCKS, TileType.GRASS, TileType.ROCKS, TileType.ROCKS],
            [TileType.ROCKS, TileType.ROCKS, TileType.GRASS, TileType.ROCKS, TileType.ROCKS],
        ],
        krecik_position=Position(2, 2),
    )


def random(width: int, height: int) -> Board:
    number_of_choices = len(TileType)
    matrix = []
    for _ in range(height):
        random_row = [TileType(randrange(number_of_choices)) for _ in range(width)]
        matrix.append(random_row)
    return Board(matrix)
