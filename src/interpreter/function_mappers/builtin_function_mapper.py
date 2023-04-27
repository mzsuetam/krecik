from typing import Callable, Type

from board.board_manager import BoardManager
from interpreter.exceptions import (
    IncorrectArgumentsNumberError,
    NotDefinedFunctionError,
)
from interpreter.krecik_types.cely import Cely
from interpreter.krecik_types.cislo import Cislo
from interpreter.krecik_types.krecik_type import KrecikType
from interpreter.utils import validate_args

BUILTIN_FUNCTION_NAMES: set = {
    "do_predu",
    "v_pravo",
    "v_zad",
    "v_levo",
    # interaction
    "wzit",
    "poloz",
    "vykop",
    "pohrbit",
    "skryt",
    "vstavej",
    "zda_trava",
    "zda_trava_pred",
    "zda_kamen",
    "zda_kamen_pred",
    "zda_kopecek",
    "zda_kopecek_pred",
    "zda_rajce",
    "zda_rajce_pred",
    "zda_muchomur",
    "zda_muchomur_pred",
    # other
    "zda_drzi_rajce",
    "zda_drzi_muchomur",
    "pockejte",
}


class BuiltinFunctionMapper:
    default_value: tuple[None, list] = None, []

    def __init__(self, board_manager: BoardManager) -> None:
        self.function_map: dict[str, tuple[Callable, list[Type[KrecikType]]]] = {
            # changing position and direction
            "do_predu": (board_manager.move_krecik_forward, [Cely]),
            "v_pravo": (board_manager.turn_krecik_right, []),
            "v_zad": (board_manager.turn_krecik_180, []),
            "v_levo": (board_manager.turn_krecik_left, []),
            # interaction with objects
            "wzit": (board_manager.krecik_pick_up, []),
            "poloz": (board_manager.krecik_put, []),
            "vykop": (board_manager.krecik_make_mound, []),
            "pohrbit": (board_manager.krecik_remove_mound, []),
            "skryt": (board_manager.krecik_hide_in_mound, []),
            "vstavej": (board_manager.krecik_get_out_of_mound, []),
            "zda_trava": (board_manager.is_krecik_on_grass, []),
            "zda_trava_pred": (board_manager.is_grass_in_front_of_krecik, []),
            "zda_kamen": (board_manager.is_krecik_on_rocks, []),
            "zda_kamen_pred": (board_manager.is_rocks_in_front_of_krecik, []),
            "zda_kopecek": (board_manager.is_krecik_on_mound, []),
            "zda_kopecek_pred": (board_manager.is_mound_in_front_of_krecik, []),
            "zda_rajce": (board_manager.is_krecik_on_tomato, []),
            "zda_rajce_pred": (board_manager.is_tomato_in_front_of_krecik, []),
            "zda_muchomur": (board_manager.is_krecik_on_mushroom, []),
            "zda_muchomur_pred": (board_manager.is_mushroom_in_front_of_krecik, []),
            # other functions
            "zda_drzi_rajce": (board_manager.is_krecik_holding_tomato, []),
            "zda_drzi_muchomur": (board_manager.is_krecik_holding_mushroom, []),
            "pockejte": (board_manager.wait, [Cislo]),
        }

    def call(self, function_name: str, krecik_args: list[KrecikType]) -> KrecikType:
        function, expected_args_types = self.function_map.get(
            function_name,
            self.default_value,
        )
        if function is None:
            raise NotDefinedFunctionError(unrecognized_function_name=function_name)

        try:
            validate_args(krecik_args, expected_args_types)
        except IncorrectArgumentsNumberError as exc:
            exc.attrs.update({"function_name": function_name})
            raise exc

        args = [krecik_arg.value for krecik_arg in krecik_args]
        return function(*args)
