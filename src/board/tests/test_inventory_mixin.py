import pytest

from board.enums import Gatherable as Gat
from board.inventory_mixin import InventoryMixin


@pytest.mark.parametrize(
    (
        "inventory_limit",
        "initial_inventory",
        "gatherable",
        "should_success",
        "expected_inventory",
    ),
    [
        (1, [], Gat.TOMATO, True, [Gat.TOMATO]),
        (1, [], Gat.MUSHROOM, True, [Gat.MUSHROOM]),
        (1, [Gat.MUSHROOM], Gat.TOMATO, False, [Gat.MUSHROOM]),
        (2, [Gat.TOMATO], Gat.TOMATO, True, [Gat.TOMATO] * 2),
        (
            None,
            [Gat.TOMATO, Gat.MUSHROOM],
            Gat.TOMATO,
            True,
            [Gat.TOMATO, Gat.MUSHROOM, Gat.TOMATO],
        ),
    ],
)
def test_inventory_append(
    inventory_limit: int | None,
    initial_inventory: list[Gat],
    gatherable: Gat,
    should_success: bool,
    expected_inventory: list[Gat],
) -> None:
    obj_with_inventory = InventoryMixin(inventory_limit)
    obj_with_inventory.inventory = initial_inventory
    result = obj_with_inventory.append_gatherable(gatherable)
    assert result is should_success
    assert obj_with_inventory.inventory == expected_inventory


@pytest.mark.parametrize(
    (
        "initial_inventory",
        "expected_gatherable",
        "expected_inventory",
    ),
    [
        ([], None, []),
        ([Gat.TOMATO], Gat.TOMATO, []),
        ([Gat.MUSHROOM], Gat.MUSHROOM, []),
        ([Gat.TOMATO] * 2, Gat.TOMATO, [Gat.TOMATO]),
    ],
)
def test_inventory_pop(
    initial_inventory: list[Gat],
    expected_gatherable: Gat | None,
    expected_inventory: list[Gat],
) -> None:
    obj_with_inventory = InventoryMixin(None)
    obj_with_inventory.inventory = initial_inventory
    gatherable = obj_with_inventory.pop_gatherable()
    assert gatherable == expected_gatherable
    assert obj_with_inventory.inventory == expected_inventory


@pytest.mark.parametrize(
    (
        "first_inventory",
        "second_inventory",
        "should_succeed",
        "expected_first_inventory",
        "expected_second_inventory",
    ),
    [
        pytest.param(
            [Gat.TOMATO],
            [],
            True,
            [],
            [Gat.TOMATO],
            id="transfer one tomato",
        ),
        pytest.param(
            [],
            [Gat.MUSHROOM],
            False,
            [],
            [Gat.MUSHROOM],
            id="transfer from empty",
        ),
        pytest.param(
            [Gat.TOMATO],
            [Gat.TOMATO],
            False,
            [Gat.TOMATO],
            [Gat.TOMATO],
            id="transfer to full",
        ),
    ],
)
def test_inventory_transfer(
    first_inventory: list[Gat],
    second_inventory: list[Gat],
    should_succeed: bool,
    expected_first_inventory: list[Gat],
    expected_second_inventory: list[Gat],
) -> None:
    obj_with_inventory_1 = InventoryMixin(inventory_limit=1)
    obj_with_inventory_1.inventory = first_inventory
    obj_with_inventory_2 = InventoryMixin(inventory_limit=1)
    obj_with_inventory_2.inventory = second_inventory
    result = obj_with_inventory_1.transfer_to(obj_with_inventory_2)
    assert result is should_succeed
    assert obj_with_inventory_1.inventory == expected_first_inventory
    assert obj_with_inventory_2.inventory == expected_second_inventory
