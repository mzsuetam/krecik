from abc import ABC

from board.board import Board


class BaseDisplay(ABC):

    def __init__(self, board: Board) -> None:
        self.board = board

    def update_krecik_position(self) -> None:
        raise NotImplementedError()

    def update_krecik_rotation(self) -> None:
        raise NotImplementedError()
