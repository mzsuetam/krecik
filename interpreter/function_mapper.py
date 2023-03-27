from typing import Callable

from board.board import Board
from interpreter.exceptions import NotDefinedFunctionError
from window.window import Window


def do_predu(board: Board, window: Window, number_of_steps: int = 1) -> None:
    board.krecik_move(int(number_of_steps))  # TODO: remove casting to int
    window.update_krecik_position(board.krecik)
    window.refresh()


def v_levo(board: Board, window: Window) -> None:
    board.krecik.turn_left()
    window.update_krecik_rotation(board.krecik)
    window.refresh()


def v_pravo(board: Board, window: Window) -> None:
    board.krecik.turn_right()
    window.update_krecik_rotation(board.krecik)
    window.refresh()


class FunctionMapper:

    BUILD_IN_FUNCTIONS = {
        "do_predu": do_predu,
        "v_levo": v_levo,
        "v_pravo": v_pravo,
    }

    def __init__(self) -> None:
        self._name_to_function_map = FunctionMapper.BUILD_IN_FUNCTIONS.copy()

    def get(self, function_name: str) -> Callable:
        function = self._name_to_function_map.get(function_name)
        if function is None:
            raise NotDefinedFunctionError()
        return function
