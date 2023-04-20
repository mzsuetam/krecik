from typing import Type

from interpreter.exceptions import KrecikVariableUndeclaredError
from interpreter.krecik_types.krecik_type import KrecikType


class VariableStack:
    def __init__(self) -> None:
        self.stack: dict[str, list[dict[str, KrecikType]]] = {}
        self.current_func_stack: list[tuple[str, int]] = []

    def get_var_value(self, var_name: str) -> KrecikType:
        var = None
        for i in range(self._get_current_stack(), -1, -1):
            var = self.stack[self._get_current_function()][i].get(var_name)
            if var is not None:
                break
        if not var:
            raise KrecikVariableUndeclaredError(name=var_name)
        return var

    def set_var_value(self, var_name: str, value: KrecikType) -> None:
        var = self.get_var_value(var_name)
        var.value = value

    def _get_current_function(self) -> str:
        return self.current_func_stack[len(self.current_func_stack) - 1][0]

    def _get_current_stack(self) -> int:
        return self.current_func_stack[len(self.current_func_stack) - 1][1]

    def enter_function(self, func_name: str) -> None:
        """
        Use to enter given function variable stack pile,
        e.g. before calling a function
        """
        # dodajemy zbiór stacków funkcji i ustawiamy ją jako aktualną
        self.stack[func_name] = [{}]
        self.current_func_stack.append((func_name, 0))

    def exit_function(self) -> None:
        """
        Use to exit function variable stack pile
        and automatically go to previous one.
        e.g. after calling a function
        """
        # usuwamy zbiór stacków funkcji i ustawiamy poprzedni jako aktualny
        key, val = self.current_func_stack.pop()
        self.stack.pop(key)

    def enter_stack(self) -> None:
        """
        Use to enter next variable stack of current function,
        e.g. before entering if body
        """
        # dodajemy stack do obecnej funkcji, ustawiamy go jako aktualny
        if len(self.current_func_stack) > 0:
            func_name, i = self.current_func_stack[len(self.current_func_stack) - 1]
            self.stack[func_name].append({})
            self.current_func_stack[len(self.current_func_stack) - 1] = (func_name, i + 1)

    def exit_stack(self) -> None:
        """
        Use to enter exit variable stack of current function
        and automatically go to previous one.
        e.g. after exiting if body
        """
        # usuwamy obecny stack z obecnej funkcji, ustawiamy poprzedni jako aktualny
        func_name, i = self.current_func_stack[len(self.current_func_stack) - 1]
        self.stack[func_name].pop()
        self.current_func_stack[len(self.current_func_stack) - 1] = (func_name, i - 1)

    def __str__(self) -> str:
        string = ""
        for key, val in self.stack.items():
            string += f"Function {key}:\n"
            for i, stack in enumerate(val):
                string += f"\tStack: {i}\n"
                for s_key, s_val in stack.items():
                    string += f"\t\t{s_val}\n"
        return string

    def declare(self, var_type: Type[KrecikType], var_name: str) -> KrecikType:
        var = var_type(None)
        # dodajemy zmienną do obecnego stacka w obecnej funkcji
        func = self._get_current_function()
        stack = self._get_current_stack()
        self.stack[func][stack][var_name] = var
        return var
