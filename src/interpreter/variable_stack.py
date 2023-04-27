from typing import Type

from interpreter.exceptions import KrecikVariableUndeclaredError, KrecikVariableStackUsageError, \
    KrecikVariableAssignedTypeError, KrecikVariableRedeclarationError
from interpreter.krecik_types.cely import Cely
from interpreter.krecik_types.cislo import Cislo
from interpreter.krecik_types.krecik_type import KrecikType
from interpreter.krecik_types.logicki import Logicki


class Frame:
    """
    Used as frame for function.
    """
    def __init__(self) -> None:
        self.subframes: list[SubFrame] = []


class SubFrame:
    """
    Used as frame for body.
    """
    def __init__(self) -> None:
        self.variables: dict[str, KrecikType] = {}


class VariableStack:
    def __init__(self) -> None:
        self.frames: list[Frame] = []

    def append_frame(self, func_name: str) -> None:
        func_frame = Frame()
        self.frames.append(func_frame)

    def pop_frame(self) -> None:
        if len(self.frames) == 0:
            raise KrecikVariableStackUsageError(failed_event="pop frame", reason="frame stack empty")
        self.frames.pop()

    def append_subframe(self) -> None:
        if len(self.frames) == 0:
            raise KrecikVariableStackUsageError(failed_event="append subframe", reason="frame stack empty")
        curr_frame = self.frames[-1]
        subframe = SubFrame()
        curr_frame.subframes.append(subframe)

    def pop_subframe(self) -> None:
        if len(self.frames) == 0:
            raise KrecikVariableStackUsageError(failed_event="pop subframe", reason="frame stack empty")
        curr_frame = self.frames[-1]
        if len(curr_frame.subframes) == 0:
            raise KrecikVariableStackUsageError(
                failed_event="pop subframe", reason="subframes stack empty"
            )
        curr_frame.subframes.pop()

    def declare_variable(self, var_type: Type[KrecikType], var_name: str) -> KrecikType:
        if len(self.frames) == 0:
            raise KrecikVariableStackUsageError(
                failed_event="declare variable", reason="frame stack empty"
            )
        curr_frame = self.frames[-1]
        if len(curr_frame.subframes) == 0:
            raise KrecikVariableStackUsageError(
                failed_event="declare variable", reason="subframes stack empty"
            )
        curr_subframe = curr_frame.subframes[-1]

        if curr_subframe.variables.get(var_name) is not None:
            raise KrecikVariableRedeclarationError(var_name=var_name)

        var = var_type(None)
        curr_subframe.variables.update({var_name: var})

        return var

    def get_var(self, var_name: str) -> KrecikType:
        if len(self.frames) == 0:
            raise KrecikVariableStackUsageError(
                failed_event="get variable value", reason="frame stack empty"
            )
        curr_frame = self.frames[-1]
        if len(curr_frame.subframes) == 0:
            raise KrecikVariableStackUsageError(
                failed_event="get variable value", reason="subframes stack empty"
            )

        for frame in reversed(curr_frame.subframes):
            var = frame.variables.get(var_name)
            if var is not None:
                return var
        raise KrecikVariableUndeclaredError(name=var_name)
