from typing import Callable

from board.board_manager import BoardManager
from interpreter.builtin_function_names import BuiltinFunctionName
from interpreter.exceptions import (
    IncorrectArgumentsNumberError,
    NotDefinedFunctionError,
)
from interpreter.krecik_types.cely import Cely
from interpreter.krecik_types.cislo import Cislo
from interpreter.krecik_types.krecik_type import KrecikType
from interpreter.utils import validate_args


class BuiltinFunctionMapper:
    def __init__(self, board_manager: BoardManager) -> None:
        self.function_map: dict[BuiltinFunctionName, tuple[Callable, list[type[KrecikType]]]] = {
            BuiltinFunctionName.do_predu: (board_manager.move_krecik_forward, [Cely]),
            BuiltinFunctionName.v_pravo: (board_manager.turn_krecik_right, []),
            BuiltinFunctionName.v_zad: (board_manager.turn_krecik_180, []),
            BuiltinFunctionName.v_levo: (board_manager.turn_krecik_left, []),
            BuiltinFunctionName.wzit: (board_manager.krecik_pick_up, []),
            BuiltinFunctionName.poloz: (board_manager.krecik_put, []),
            BuiltinFunctionName.vykop: (board_manager.krecik_make_mound, []),
            BuiltinFunctionName.pohrbit: (board_manager.krecik_remove_mound, []),
            BuiltinFunctionName.skryt: (board_manager.krecik_hide_in_mound, []),
            BuiltinFunctionName.vstavej: (board_manager.krecik_get_out_of_mound, []),
            BuiltinFunctionName.zda_trava: (board_manager.is_krecik_on_grass, []),
            BuiltinFunctionName.zda_trava_pred: (board_manager.is_grass_in_front_of_krecik, []),
            BuiltinFunctionName.zda_kamen: (board_manager.is_krecik_on_rocks, []),
            BuiltinFunctionName.zda_kamen_pred: (board_manager.is_rocks_in_front_of_krecik, []),
            BuiltinFunctionName.zda_kopecek: (board_manager.is_krecik_on_mound, []),
            BuiltinFunctionName.zda_kopecek_pred: (board_manager.is_mound_in_front_of_krecik, []),
            BuiltinFunctionName.zda_rajce: (board_manager.is_krecik_on_tomato, []),
            BuiltinFunctionName.zda_rajce_pred: (board_manager.is_tomato_in_front_of_krecik, []),
            BuiltinFunctionName.zda_muchomur: (board_manager.is_krecik_on_mushroom, []),
            BuiltinFunctionName.zda_muchomur_pred: (
                board_manager.is_mushroom_in_front_of_krecik,
                [],
            ),
            BuiltinFunctionName.zda_drzi_rajce: (board_manager.is_krecik_holding_tomato, []),
            BuiltinFunctionName.zda_drzi_muchomur: (board_manager.is_krecik_holding_mushroom, []),
            BuiltinFunctionName.pockejte: (board_manager.wait, [Cislo]),
        }

    def call(self, function_name: str, krecik_args: list[KrecikType]) -> KrecikType:
        try:
            name = BuiltinFunctionName[function_name]
            function, expected_args_types = self.function_map[name]
        except KeyError:
            raise NotDefinedFunctionError(unrecognized_function_name=function_name)

        try:
            validate_args(krecik_args, expected_args_types)
        except IncorrectArgumentsNumberError as exc:
            exc.attrs.update({"function_name": function_name})
            raise exc

        args = [krecik_arg.value for krecik_arg in krecik_args]
        return function(*args)
