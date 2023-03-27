import pytest as pytest

from board.board import Board
from board.krecik import Position, Rotation
from board.tile import Gatherable, Terrain, TileType


@pytest.mark.parametrize(
    ("initial_rotation", "expected_position"),
    [
        (Rotation.N, Position(col=0, row=0)),
        (Rotation.E, Position(col=1, row=0)),
        (Rotation.S, Position(col=0, row=0)),
        (Rotation.W, Position(col=0, row=0)),
    ],
    ids=[
        "krecik hit north border",
        "krecik moves to other tile",
        "krecik hit rocks",
        "krecik hit west border",
    ],
)
def test_krecik_move(
    initial_rotation: Rotation,
    expected_position: Position
) -> None:
    matrix = [
        [TileType.GRASS, TileType.GRASS],
        [TileType.ROCKS, TileType.TOMATO],
    ]
    board = Board(matrix)
    board.krecik.rotation = initial_rotation
    board.krecik_move()
    assert board.krecik.position == expected_position


@pytest.mark.parametrize(
    ("tile_type", "expected_inventory"),
    [
        (TileType.GRASS, []),
        (TileType.TOMATO, [Gatherable.TOMATO]),
        (TileType.MUSHROOM, [Gatherable.MUSHROOM]),
    ],
    ids=[
        "krecik cant pick up grass",
        "krecik picks up tomato",
        "krecik picks up mushroom",
    ],
)
def test_krecik_pick(
    tile_type: TileType,
    expected_inventory: list[Gatherable],
) -> None:
    matrix = [[tile_type]]
    board = Board(matrix)
    board.krecik_pick()
    assert board.krecik.inventory == expected_inventory
    assert board.get_krecik_tile().gatherable is None
    assert board.get_krecik_tile().terrain is Terrain.GRASS


def test_krecik_pickup_limit() -> None:
    matrix = [[TileType.TOMATO]]
    board = Board(matrix)
    assert board.krecik.inventory_limit == 1
    board.krecik.inventory = [Gatherable.MUSHROOM]
    board.krecik_pick()
    assert board.krecik.inventory == [Gatherable.MUSHROOM]
    assert board.get_krecik_tile().gatherable == Gatherable.TOMATO


@pytest.mark.parametrize(
    ("tile_type", "expected_inventory", "expected_tile_gatherable"),
    [
        (TileType.GRASS, [], Gatherable.MUSHROOM),
        (TileType.TOMATO, [Gatherable.MUSHROOM], Gatherable.TOMATO),
        (TileType.MUSHROOM, [Gatherable.MUSHROOM], Gatherable.MUSHROOM),
    ],
    ids=[
        "krecik puts mushroom on grass",
        "krecik cant put mushroom on tomato",
        "krecik cant put mushroom on mushroom",
    ],
)
def test_krecik_put(
    tile_type: TileType,
    expected_inventory: list[Gatherable],
    expected_tile_gatherable: Gatherable,
) -> None:
    matrix = [[tile_type]]
    board = Board(matrix)
    board.krecik.inventory = [Gatherable.MUSHROOM]
    board.krecik_put()
    assert board.krecik.inventory == expected_inventory
    assert board.get_krecik_tile().gatherable == expected_tile_gatherable


def test_krecik_put_nothing() -> None:
    matrix = [[TileType.GRASS]]
    board = Board(matrix)
    board.krecik.inventory = []
    board.krecik_put()
    assert board.krecik.inventory == []
    assert board.get_krecik_tile().gatherable is None
