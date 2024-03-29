from board.board import Board
from display.base_display import BaseDisplay


class TerminalDisplay(BaseDisplay):
    def __init__(self, board: Board) -> None:
        super().__init__(board)
        print(
            "=== new board ===",
            f"- width: {board.width}",
            f"- height: {board.height}",
            "- krecik: ",
            f"\t- {board.krecik.position}",
            f"\t- {board.krecik.rotation}",
            sep="\n",
        )

    def update_krecik_position(self) -> None:
        print(f"krecik moves to {self.board.krecik.position}")

    def update_krecik_rotation(self) -> None:
        print(f"krecik face {self.board.krecik.rotation}")

    def update_make_mound(self) -> None:
        print(f"krecik makes mound at {self.board.krecik.position}")

    def update_remove_mound(self) -> None:
        print(f"krecik removes mound at {self.board.krecik.position}")

    def update_hide(self) -> None:
        print(f"krecik hides in mound at {self.board.krecik.position}")

    def update_get_out(self) -> None:
        print(f"krecik gets out from mound at {self.board.krecik.position}")
