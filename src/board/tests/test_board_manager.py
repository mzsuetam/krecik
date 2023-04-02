from unittest.mock import Mock

import pytest as pytest

from board.board import Board
from board.board_examples import plains
from board.board_manager import BoardManager
from board.krecik import Position, Rotation
from board.tests.conftest import check_publisher_notify
from board.tile import Gatherable, Terrain, TileType
from display.board_publisher import EventType


@pytest.mark.parametrize(
    ("initial_rotation", "expected_position", "should_notify"),
    [
        (Rotation.N, Position(col=0, row=0), False),
        (Rotation.E, Position(col=1, row=0), True),
        (Rotation.S, Position(col=0, row=0), False),
        (Rotation.W, Position(col=0, row=0), False),
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
    expected_position: Position,
    should_notify: bool,
    board_publisher_mock: Mock,
) -> None:
    matrix = [
        [TileType.GRASS, TileType.GRASS],
        [TileType.ROCKS, TileType.TOMATO],
    ]
    board = Board(matrix)
    board_manager = BoardManager(board, board_publisher_mock)
    board.krecik.rotation = initial_rotation

    board_manager.move_forward(1)

    assert board.krecik.position == expected_position
    assert check_publisher_notify(
        board_publisher_mock,
        EventType.POSITION,
        should_notify,
    )


@pytest.mark.parametrize(
    ("method_name", "expected_rotation"),
    [
        ("turn_right", Rotation.E),
        ("turn_180", Rotation.S),
        ("turn_left", Rotation.W),
    ],
)
def test_krecik_rotate(
    method_name: str,
    expected_rotation: Rotation,
    board_publisher_mock: Mock,
) -> None:
    board = plains(1, 1)
    board_manager = BoardManager(board, board_publisher_mock)
    board.krecik.rotation = Rotation.N

    getattr(board_manager, method_name)()

    assert board.krecik.rotation == expected_rotation
    assert check_publisher_notify(
        board_publisher_mock,
        EventType.ROTATION,
    )


@pytest.mark.parametrize(
    ("tile_type", "expected_inventory", "should_notify"),
    [
        (TileType.GRASS, [], False),
        (TileType.TOMATO, [Gatherable.TOMATO], True),
        (TileType.MUSHROOM, [Gatherable.MUSHROOM], True),
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
    should_notify: bool,
    board_publisher_mock: Mock,
) -> None:
    matrix = [[tile_type]]
    board = Board(matrix)
    board_manager = BoardManager(board, board_publisher_mock)

    board_manager.pick_up()

    assert board.krecik.inventory == expected_inventory
    assert board.get_krecik_tile().gatherable is None
    assert board.get_krecik_tile().terrain is Terrain.GRASS
    assert check_publisher_notify(
        board_publisher_mock,
        EventType.PICK,
        should_notify,
    )


def test_krecik_pickup_limit(board_publisher_mock: Mock) -> None:
    matrix = [[TileType.TOMATO]]
    board = Board(matrix)
    board_manager = BoardManager(board, board_publisher_mock)
    assert board.krecik.inventory_limit == 1
    board.krecik.inventory = [Gatherable.MUSHROOM]

    board_manager.pick_up()

    assert board.krecik.inventory == [Gatherable.MUSHROOM]
    assert board.get_krecik_tile().gatherable == Gatherable.TOMATO
    board_publisher_mock.notify.assert_not_called()


@pytest.mark.parametrize(
    (
        "tile_type",
        "expected_inventory",
        "expected_tile_gatherable",
        "should_notify",
    ),
    [
        (TileType.GRASS, [], Gatherable.MUSHROOM, True),
        (TileType.TOMATO, [Gatherable.MUSHROOM], Gatherable.TOMATO, False),
        (TileType.MUSHROOM, [Gatherable.MUSHROOM], Gatherable.MUSHROOM, False),
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
    should_notify: bool,
    board_publisher_mock: Mock,
) -> None:
    matrix = [[tile_type]]
    board = Board(matrix)
    board_manager = BoardManager(board, board_publisher_mock)
    board.krecik.inventory = [Gatherable.MUSHROOM]

    board_manager.put()

    assert board.krecik.inventory == expected_inventory
    assert board.get_krecik_tile().gatherable == expected_tile_gatherable
    assert check_publisher_notify(
        board_publisher_mock,
        EventType.PUT,
        should_notify,
    )


def test_krecik_put_nothing(board_publisher_mock: Mock) -> None:
    board = plains(1, 1)
    board_manager = BoardManager(board, board_publisher_mock)
    board.krecik.inventory = []

    board_manager.put()

    assert board.krecik.inventory == []
    assert board.get_krecik_tile().gatherable is None
    board_publisher_mock.notify.assert_not_called()
