from dataclasses import dataclass
from enum import Enum

from board.inventory_mixin import InventoryMixin


@dataclass
class Position:
    col: int
    row: int


class Rotation(Enum):
    N = 0
    E = 1
    S = 2
    W = 3


class Krecik(InventoryMixin):

    def __init__(
        self,
        position: Position | None = None,
        rotation: Rotation | None = None,
    ) -> None:
        super().__init__()
        self._position = position or Position(0, 0)
        self.rotation = rotation or Rotation.S
        self.is_in_mound = False

    @property
    def position(self) -> Position:
        return self._position

    @position.setter
    def position(self, new_position: Position) -> None:
        self._position = new_position
        self.is_in_mound = False

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
