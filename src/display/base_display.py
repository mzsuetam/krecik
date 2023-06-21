from abc import ABC, abstractmethod

from board.board import Board


class BaseDisplay(ABC):
    def __init__(self, board: Board) -> None:
        self.board = board

    @abstractmethod
    def update_krecik_position(self) -> None:
        pass

    @abstractmethod
    def update_krecik_rotation(self) -> None:
        pass

    @abstractmethod
    def update_make_mound(self) -> None:
        pass

    @abstractmethod
    def update_remove_mound(self) -> None:
        pass

    @abstractmethod
    def update_hide(self) -> None:
        pass

    @abstractmethod
    def update_get_out(self) -> None:
        pass
