from typing import Callable, Type

from antlr.KrecikParser import KrecikParser
from board.board_manager import BoardManager
from interpreter.exceptions import (
    IncorrectArgumentTypeError,
    IncorrectArgumentsNumberError,
    NotDefinedFunctionError,
    NullArgumentError,
)
from interpreter.krecik_types.cely import Cely
from interpreter.krecik_types.cislo import Cislo
from interpreter.krecik_types.krecik_type import KrecikType


class FunctionMapper:
    default_built_in_value: tuple[None, list] = None, []
    default_declared_value: tuple[None, list, None] = None, [], None

    def __init__(self, board_manager: BoardManager) -> None:
        self.build_in_function_map: dict[str, tuple[Callable, list[Type[KrecikType]]]] = {
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

        self.declared_function_map: dict[
            str,
            tuple[
                KrecikParser.Function_declarationContext, list[Type[KrecikType]], KrecikType | None
            ],
        ] = {}

        self._is_returning = False

    def callBuiltin(self, function_name: str, krecik_args: list[KrecikType]) -> KrecikType:
        function, expected_args_types = self.build_in_function_map.get(
            function_name,
            self.default_built_in_value,
        )
        if function is None:
            raise NotDefinedFunctionError(unrecognized_function_name=function_name)

        try:
            self.validate_args(krecik_args, expected_args_types)
        except IncorrectArgumentsNumberError as exc:
            exc.attrs.update({"function_name": function_name})
            raise exc

        args = [krecik_arg.value for krecik_arg in krecik_args]
        return function(*args)

    @staticmethod
    def validate_args(
        args: list[KrecikType],
        expected_args_types: list[Type[KrecikType]],
    ) -> None:
        if len(args) != len(expected_args_types):
            raise IncorrectArgumentsNumberError(
                expected=len(expected_args_types),
                got=len(args),
            )
        parsed_args = []
        for arg, expected_arg_type in zip(args, expected_args_types):
            if isinstance(arg, expected_arg_type):
                parsed_args.append(arg)
                continue
            if arg is not None:
                raise IncorrectArgumentTypeError(
                    expected=expected_arg_type.type_name,
                    got=arg.type_name,
                )
            else:
                raise NullArgumentError(expected=expected_arg_type.type_name)

    def is_returning(self) -> bool:
        return self._is_returning

    def init_returning(self) -> None:
        if self._is_returning:
            raise Exception()
        self._is_returning = True

    def reset_returning(self) -> None:
        if not self._is_returning:
            raise Exception()
        self._is_returning = False
