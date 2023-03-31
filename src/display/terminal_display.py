from board.krecik import Krecik
from display.base_display import BaseDisplay


class TerminalDisplay(BaseDisplay):

    def update_krecik_position(self, krecik: Krecik) -> None:
        print(f"krecik moves to (col:{krecik.position.col}, row:{krecik.position.row})")

    def update_krecik_rotation(self, krecik: Krecik) -> None:
        print(f"krecik face {krecik.rotation.name}")
