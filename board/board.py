from .krecik import Krecik, Position, Rotation
from .tile import Tile, TileType


class Board:
    """
    self.matrix is list of rows, row is list of Tiles
    """

    def __init__(
        self,
        matrix: list[list[TileType]],
        krecik_position: Position | None = None,
        krecik_rotation: Rotation | None = None,
    ) -> None:
        self.krecik = Krecik(
            position=krecik_position,
            rotation=krecik_rotation,
        )
        self.width = len(matrix[0])
        self.height = len(matrix)
        self.matrix: list[list[Tile]] = []
        for row in matrix:
            tiles_row = [Tile(value) for value in row]
            if len(tiles_row) != self.width:
                raise RuntimeError("Rows have not matching length!")
            self.matrix.append(tiles_row)

    def get(self, row: int, col: int) -> Tile | None:
        if not self._is_cords_valid(row=row, col=col):
            return None
        return self.matrix[row][col]

    def _is_cords_valid(self, col: int, row: int) -> bool:
        if not (0 <= row < self.height):
            return False
        if not (0 <= col < self.width):
            return False
        return True

    def krecik_move(self, tiles_number: int = 1) -> None:
        for _ in range(tiles_number):
            self._make_move()

    def _make_move(self) -> None:
        new_pos = self.krecik.next_position()
        if not self._is_cords_valid(row=new_pos.row, col=new_pos.col):
            return
        if not (new_tile := self.get(row=new_pos.row, col=new_pos.col)):
            return
        if not new_tile.can_step_on():
            return
        self.krecik.position = new_pos

    def krecik_pick(self) -> None:
        tile = self.get_krecik_tile()
        if self.krecik.can_pick() and tile.gatherable is not None:
            gatherable = tile.pick()
            self.krecik.inventory.append(gatherable)

    def krecik_put(self) -> None:
        tile = self.get_krecik_tile()
        if tile.gatherable is None:
            gatherable = self.krecik.pop_from_inventory()
            tile.gatherable = gatherable

    def get_krecik_tile(self) -> Tile:
        pos = self.krecik.position
        return self.matrix[pos.row][pos.col]

    def __repr__(self) -> str:
        return f"<Board {self.width}x{self.height}>"
