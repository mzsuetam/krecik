from dataclasses import dataclass
from typing import TypeAlias

from antlr.KrecikParser import KrecikParser
from interpreter.exceptions import KrecikFunctionRedeclarationError, KrecikFunctionUndeclaredError
from interpreter.krecik_types.krecik_type import KrecikType


@dataclass(frozen=True)
class FunctionDeclaration:
    context: KrecikParser.Function_declarationContext
    arg_types: list[type[KrecikType]]
    return_type: type[KrecikType]


FunctionMap: TypeAlias = dict[str, FunctionDeclaration]


class DeclaredFunctionMapper:
    def __init__(self) -> None:
        self.function_map: FunctionMap = {}
        self._is_returning = False

    def declare_function(
        self,
        name: str,
        ctx: KrecikParser.Function_declarationContext,
        arg_types: list[type[KrecikType]],
        return_type: type[KrecikType],
    ) -> None:
        if self.function_map.get(name) is not None:
            raise KrecikFunctionRedeclarationError(name=name)

        self.function_map[name] = FunctionDeclaration(ctx, arg_types, return_type)

    def get_function(self, name: str) -> FunctionDeclaration:
        function = self.function_map.get(name)
        if function is None:
            raise KrecikFunctionUndeclaredError(name=name)
        return function

    def clear(self) -> None:
        self.function_map.clear()

    def is_returning(self) -> bool:
        return self._is_returning

    def init_returning(self) -> None:
        if self._is_returning:
            raise RuntimeError("should not get here")
        self._is_returning = True

    def reset_returning(self) -> None:
        if not self._is_returning:
            raise RuntimeError("should not get here")
        self._is_returning = False
