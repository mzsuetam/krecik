from interpreter.exceptions import KrecikException, KrecikVariableUnassignedError, KrecikVariableUndeclaredError
from interpreter.krecik_types.krecik_type import KrecikType


class VariableStack:

    stack: dict[str, list[dict[str, KrecikType]]] = {}

    current_func_stack = []

    def getVarValue(self, var_name: str) -> KrecikType:
        # print(f"Accessed: {var_name} of func {self.__getCurrFunction()} stack {self.__getCurrStack()}")
        var = None
        try:
            # var = self.stack.get(self.__getCurrFunction())[self.__getCurrStack()].get(var_name)
            for i in range(self.__getCurrStack(),-1,-1):
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
            for i in range(self.__getCurrStack(),-1,-1):
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
        self.current_func_stack.append((func_name, 0))

    def exitFunction(self):
        """
            Use to exit function variable stack pile
            and automatically go to previous one.
            e.g. after calling a function
        """
        self.current_func_stack.pop()

    def enterStack(self):
        """
            Use to enter next variable stack of current function,
            e.g. before entering if body
        """
        if len(self.current_func_stack) > 0:
            func_name, i = self.current_func_stack[len(self.current_func_stack)-1]
            self.current_func_stack[len(self.current_func_stack) - 1] = (func_name, i+1)

    def exitStack(self):
        """
            Use to enter exit variable stack of current function
            and automatically go to previous one.
            e.g. after exiting if body
        """
        func_name, i = self.current_func_stack[len(self.current_func_stack)-1]
        self.current_func_stack[len(self.current_func_stack) - 1] = (func_name, i-1)

    def __str__(self):
        str = ""
        for key, val in self.stack.items():
            str += f"Function {key}:\n"
            for i, stack in enumerate(val):
                str += f"\tStack: {i}\n"
                for s_key, s_val in stack.items():
                    str += f"\t\t{s_val}\n"
        return str

