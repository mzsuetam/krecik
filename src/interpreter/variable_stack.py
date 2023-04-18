from interpreter.exceptions import KrecikException, KrecikVariableUnassignedError, KrecikVariableUndeclaredError
from interpreter.krecik_types.cely import Cely
from interpreter.krecik_types.cislo import Cislo
from interpreter.krecik_types.krecik_type import KrecikType
from interpreter.krecik_types.logicki import Logicki


class VariableStack:

    def __init__(self) -> None:
        self.stack: dict[str, list[dict[str, KrecikType]]] = {}
        self.current_func_stack: list[tuple[str, int]] = []

    def getVarValue(self, var_name: str) -> KrecikType:
        # print(f"Accessed: {var_name} of func {self.__getCurrFunction()} stack {self.__getCurrStack()}")
        var = None
        try:
            # var = self.stack.get(self.__getCurrFunction())[self.__getCurrStack()].get(var_name)
            for i in range(self.__getCurrStack(), -1, -1):
                var = self.stack.get(self.__getCurrFunction())[i].get(var_name)
                if var is not None:
                    break
        except Exception as e:
            raise KrecikException()
        if not var:
            raise KrecikVariableUndeclaredError(name=var_name)
        return var

    def setVarValue(self, var_name, value) -> None:
        var = None
        try:
            # var = self.stack.get(self.__getCurrFunction())[self.__getCurrStack()].get(var_name)
            for i in range(self.__getCurrStack(), -1, -1):
                var = self.stack.get(self.__getCurrFunction())[i].get(var_name)
                if var is not None:
                    break
        except:
            raise KrecikException()
        if not var:
            raise KrecikVariableUndeclaredError(name=var_name)
        var.value = value

    def __getCurrFunction(self):
        return self.current_func_stack[len(self.current_func_stack)-1][0]

    def __getCurrStack(self):
        return self.current_func_stack[len(self.current_func_stack)-1][1]

    def enterFunction(self, func_name: str):
        """
            Use to enter given function variable stack pile,
            e.g. before calling a function
        """
        # dodajemy zbiór stacków funkcji i ustawiamy ją jako aktualnyą
        self.stack.update({func_name: []})
        self.stack.get(func_name).append({})
        self.current_func_stack.append((func_name, 0))

    def exitFunction(self):
        """
            Use to exit function variable stack pile
            and automatically go to previous one.
            e.g. after calling a function
        """
        # usuwamy zbiór stacków funkcji i ustawiamy poprzedni jako aktualny
        key, val = self.current_func_stack.pop()
        self.stack.pop(key)

    def enterStack(self):
        """
            Use to enter next variable stack of current function,
            e.g. before entering if body
        """
        # dodajemy stack do obecnej funkcji, ustawiamy go jako aktualny
        if len(self.current_func_stack) > 0:
            func_name, i = self.current_func_stack[len(self.current_func_stack)-1]
            self.stack.get(func_name).append({})
            self.current_func_stack[len(self.current_func_stack) - 1] = (func_name, i+1)

    def exitStack(self):
        """
            Use to enter exit variable stack of current function
            and automatically go to previous one.
            e.g. after exiting if body
        """
        # usuwamy obecny stack z obecnej funkcji, ustawiamy poprzedni jako aktualny
        func_name, i = self.current_func_stack[len(self.current_func_stack)-1]
        self.stack.get(func_name).pop()
        self.current_func_stack[len(self.current_func_stack) - 1] = (func_name, i-1)

    def __str__(self):
        string = ""
        for key, val in self.stack.items():
            string += f"Function {key}:\n"
            for i, stack in enumerate(val):
                string += f"\tStack: {i}\n"
                for s_key, s_val in stack.items():
                    string += f"\t\t{s_val}\n"
        return string

    def declare(self, var_type: str, var_name: str) -> KrecikType:
        var: KrecikType | None = None
        if var_type == Cely.type_name:
            var = Cely(None, var_name)
        if var_type == Cislo.type_name:
            var = Cislo(None, var_name)
        if var_type == Logicki.type_name:
            var = Logicki(None, var_name)
        if not var:
            raise KrecikException()

        # dodajemy zmienną do obecnego stacka w obecnej funkcji
        func = self.__getCurrFunction()
        stack = self.__getCurrStack()
        self.stack.get(func)[stack].update({var_name: var})
        return var
