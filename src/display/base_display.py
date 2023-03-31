from abc import ABC

from board.krecik import Krecik


class BaseDisplay(ABC):

    def update_krecik_position(self, krecik: Krecik) -> None:
        raise NotImplementedError()

    def update_krecik_rotation(self, krecik: Krecik) -> None:
        raise NotImplementedError()
