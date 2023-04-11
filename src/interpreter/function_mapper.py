from typing import Any, Callable

from board.board_manager import BoardManager
from interpreter.exceptions import IncorrectArgumentsNumberError, NotDefinedFunctionError


class FunctionMapper:

    def __init__(self, board_manager: BoardManager) -> None:
        self.build_in_function_map: dict[str, Callable] = {
            # changing position and direction
            "do_predu": board_manager.move_krecik_forward,
            "v_pravo": board_manager.turn_krecik_right,
            "v_zad": board_manager.turn_krecik_180,
            "v_levo": board_manager.turn_krecik_left,
            # interaction with objects
            "wzit": board_manager.krecik_pick_up,
            "poloz": board_manager.krecik_put,
            "vykop": board_manager.krecik_make_mound,
            "pohrbit": board_manager.krecik_remove_mound,
            "skryt": board_manager.krecik_hide_in_mound,
            "vstavej": board_manager.krecik_get_out_of_mound,
            "zda_trava": board_manager.is_krecik_on_grass,
            "zda_trava_pred": board_manager.is_grass_in_front_of_krecik,
            "zda_kamen": board_manager.is_krecik_on_rocks,
            "zda_kamen_pred": board_manager.is_rocks_in_front_of_krecik,
            "zda_kopecek": board_manager.is_krecik_on_mound,
            "zda_kopecek_pred": board_manager.is_mound_in_front_of_krecik,
            "zda_rajce": board_manager.is_krecik_on_tomato,
            "zda_rajce_pred": board_manager.is_tomato_in_front_of_krecik,
            "zda_muchomur": board_manager.is_krecik_on_mushroom,
            "zda_muchomur_pred": board_manager.is_mushroom_in_front_of_krecik,
            # other functions
            "zda_drzi_rajce": board_manager.is_krecik_holding_tomato,
            "zda_drzi_muchomur": board_manager.is_krecik_holding_mushroom,
            "pockejte": board_manager.wait,
        }

    def call(self, function_name: str, *args: Any) -> Callable:
        if function := self.build_in_function_map.get(function_name, None):
            try:
                return function(*args)
            except TypeError as e:
                raise IncorrectArgumentsNumberError(e)
        raise NotDefinedFunctionError()
