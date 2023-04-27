from typing import Type, TypeAlias

from antlr.KrecikParser import KrecikParser
from interpreter.exceptions import KrecikFunctionRedeclarationError
from interpreter.krecik_types.krecik_type import KrecikType

FunctionMapItem: TypeAlias = tuple[
    KrecikParser.Function_declarationContext, list[type[KrecikType]], type[KrecikType] | None
]

FunctionMap: TypeAlias = dict[str, FunctionMapItem]


class DeclaredFunctionMapper:
    def __init__(self) -> None:
        self.function_map: FunctionMap = {}

        self._is_returning = False

    def declare_function(
        self,
        name: str,
        ctx: KrecikParser.Function_declarationContext,
        arg_types: list[Type[KrecikType]],
        return_type: type[KrecikType],
    ) -> None:
        if self.function_map.get(name) is not None:
            raise KrecikFunctionRedeclarationError(name=name)

        function = ctx, arg_types, return_type
        self.function_map[name] = function

    def get_function(self, name: str) -> FunctionMapItem | None:
        return self.function_map.get(name)

    def clear(self) -> None:
        self.function_map.clear()

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
