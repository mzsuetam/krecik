from random import choice, randrange

from board.board import Board
from board.krecik import Krecik, Position
from board.tile import TileType


def plains(width: int = 16, height: int = 10) -> Board:
    return Board([[TileType.GRASS] * width] * height)


def jebus_cross(width: int = 7, height: int = 7) -> Board:
    matrix = []
    for h in range(height):
        if h == height // 2:
            random_row = [TileType.GRASS for _ in range(width)]
        else:
            random_row = [
                TileType.GRASS if w == width // 2 else TileType.ROCKS for w in range(width)
            ]
        matrix.append(random_row)
    krecik_col = width // 2
    krecik_row = height // 2
    return Board(matrix, krecik=Krecik(position=Position(krecik_col, krecik_row)))


def random(width: int = 16, height: int = 10) -> Board:
    choices = [tile_type.value for tile_type in TileType]
    matrix = []
    for _ in range(height):
        random_row = [TileType(choice(choices)) for _ in range(width)]
        matrix.append(random_row)
    krecik_col = randrange(width - 1)
    krecik_row = randrange(height - 1)
    return Board(matrix, krecik=Krecik(position=Position(krecik_col, krecik_row)))
