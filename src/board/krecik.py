from dataclasses import dataclass
from enum import Enum, auto
from board.tile import Gatherable


@dataclass
class Position:
    col: int
    row: int


class Rotation(Enum):
    N = auto()
    E = auto()
    S = auto()
    W = auto()


class Krecik:

    def __init__(
        self,
        position: Position | None = None,
        rotation: Rotation | None = None,
        inventory_limit: int = 1,
    ) -> None:
        self.position = position or Position(0, 0)
        self.rotation = rotation or Rotation.S
        self.inventory: list[Gatherable] = []
        self.inventory_limit = inventory_limit

    def rotate(self, value: int) -> None:
        new_rotation_value = (self.rotation.value + value) % len(Rotation)
        self.rotation = Rotation(new_rotation_value)

    def next_position(self) -> Position:
        if self.rotation == Rotation.N:
            return Position(
                row=self.position.row - 1,
                col=self.position.col,
            )
        if self.rotation == Rotation.E:
            return Position(
                row=self.position.row,
                col=self.position.col + 1,
            )
        if self.rotation == Rotation.S:
            return Position(
                row=self.position.row + 1,
                col=self.position.col,
            )
        if self.rotation == Rotation.W:
            return Position(
                row=self.position.row,
                col=self.position.col - 1,
            )
        raise NotImplementedError()

    def can_pick(self) -> bool:
        return len(self.inventory) < self.inventory_limit

    def pop_from_inventory(self) -> Gatherable | None:
        if self.inventory:
            return self.inventory.pop()
        return None
