from board.krecik import Krecik, Position, Rotation
from board.tile import Tile, TileType


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
        self.matrix: list[list[Tile]] = self._init_matrix(matrix)

    def _init_matrix(self, matrix: list[list[TileType]]) -> list[list[Tile]]:
        result_matrix = []
        for row in matrix:
            tiles_row = [Tile(value) for value in row]
            if len(tiles_row) != self.width:
                raise RuntimeError("Rows have not matching length!")
            result_matrix.append(tiles_row)
        return result_matrix

    def get_krecik_tile(self) -> Tile:
        pos = self.krecik.position
        return self.matrix[pos.row][pos.col]

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

    def __repr__(self) -> str:
        return f"<Board {self.width}x{self.height}>"
