from typing import Any


class KrecikException(Exception):
    message_schema: str = "Error occurred."
    attrs: dict[str, Any] = {}

    def __init__(self, **kwargs: Any) -> None:
        self.attrs.update(kwargs)
        self.start_line: int | None = None
        self.stop_line: int | None = None
        self.start_column: int | None = None
        self.stop_column: int | None = None

    @property
    def message(self) -> str:
        return self.message_schema.format(**self.attrs)

    def __str__(self) -> str:
        line_info = self.line_info()
        column_info = self.column_info()
        return f"\033[91mPozor {line_info}, {column_info}!!!\n\t{self.message}\033[0m"

    def line_info(self) -> str:
        if self.start_line is None or self.stop_line is None:
            return ""
        if self.start_line == self.stop_line:
            return f"linka: {self.start_line}"
        return f"linky: {self.start_line}-{self.stop_line}"

    def column_info(self) -> str:
        if self.start_column is None or self.stop_column is None:
            return ""
        if self.start_column == self.stop_column:
            return f"sloupec: {self.start_column}"
        return f"sloupce: {self.start_column}-{self.stop_column}"


class NotDefinedFunctionError(KrecikException):
    message_schema = "Function `{unrecognized_function_name}` is not defined."
    attrs = {"unrecognized_function_name": "not specified"}


class IncorrectArgumentsNumberError(KrecikException):
    message_schema = (
        "Incorrect number of arguments. Function {function_name} "
        "expects {expected} arguments, but got {got}."
    )
    attrs = {
        "function_name": "not specified",
        "expected": "not specified",
        "got": "not specified",
    }


class IncorrectArgumentTypeError(KrecikException):
    message_schema = "Incorrect argument type. Expected {expected}, got {got}."
    attrs = {"expected": "not specified", "got": "not specified"}


class KrecikValueError(KrecikException):
    message_schema = "Invalid value for {type_name}: {value}."
    attrs = {"type_name": "not specified", "value": "not specified"}
