from typing import Any, Callable

from board.board_manager import BoardManager
from interpreter.exceptions import IncorrectArgumentsNumberError, NotDefinedFunctionError


class FunctionMapper:

    def __init__(self, board_manager: BoardManager) -> None:
        self.build_in_function_map: dict[str, Callable] = {
            "do_predu": board_manager.move_forward,
            "v_levo": board_manager.turn_left,
            "v_pravo": board_manager.turn_right,
            "pockejte": board_manager.wait,
            "wzit": board_manager.pick_up,
            "poloz": board_manager.put,
        }

    def call(self, function_name: str, *args: Any) -> Callable:
        if function := self.build_in_function_map.get(function_name, None):
            try:
                return function(*args)
            except TypeError as e:
                raise IncorrectArgumentsNumberError(e)
        raise NotDefinedFunctionError()
