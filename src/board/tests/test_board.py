import pytest

from board.board import Board
from board.enums import TileType
from board.tests.board_examples import plains
from board.tile import Tile


@pytest.mark.parametrize(
    ("row", "col", "expected_tile_type"),
    [
        (0, 0, TileType.GRASS),
        (0, 1, TileType.TOMATO),
        (1, 0, TileType.MOUND),
        (1, 1, TileType.ROCKS),
    ],
)
def test_board_get_tile(row: int, col: int, expected_tile_type: TileType) -> None:
    matrix = [
        [TileType.GRASS, TileType.TOMATO],
        [TileType.MOUND, TileType.ROCKS],
    ]
    board = Board(matrix)
    tile = board.get_tile(row, col)
    expected_tile = Tile(expected_tile_type)
    assert tile.terrain == expected_tile.terrain  # type: ignore[union-attr]
    assert tile.inventory == expected_tile.inventory  # type: ignore[union-attr]


@pytest.mark.parametrize(
    ("row", "col"),
    [
        (-1, -1),
        (-1, 0),
        (-1, 0),
        (1, 2),
        (2, 1),
        (0, 2),
        (2, 0),
        (2, 2),
        (21241213, 132124124),
    ],
)
def test_board_get_tile_incorrect(
    row: int,
    col: int,
) -> None:
    board = plains(1, 1)
    tile = board.get_tile(row, col)
    assert tile is None
