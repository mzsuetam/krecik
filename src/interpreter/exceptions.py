from typing import Any

from antlr4 import ParserRuleContext


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
        if not line_info:
            return f"\033[91mPozor!!!\n\t{self.message}\033[0m"
        elif not column_info:
            return f"\033[91mPozor {line_info}!!!\n\t{self.message}\033[0m"
        else:
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

    def inject_context_to_exc(self, ctx: "ParserRuleContext") -> None:
        if self.start_line is not None or self.stop_line is not None:
            return
        self.start_line = ctx.start.line
        self.stop_line = ctx.stop.line
        self.start_column = ctx.start.column
        self.stop_column = ctx.stop.column


# LEXER EXCEPTIONS
class KrecikRecognitionError(KrecikException):
    message_schema = "Recognition error. {extra_info}"
    attrs = {"extra_info": "not specified"}


class KrecikNoViableAltException(KrecikRecognitionError):
    message_schema = "No viable alternative at input '{offending_symbol}'."
    attrs = {"offending_symbol": "not specified"}


class KrecikInputMismatchException(KrecikRecognitionError):
    pass


class KrecikFailedPredicateException(KrecikRecognitionError):
    pass


# PARSER EXCEPTIONS
class KrecikSyntaxError(KrecikException):
    message_schema = "Syntax error. {extra_info}"
    attrs = {"extra_info": "not specified"}


# LISTENER AND VISITOR EXCEPTIONS
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


class NullArgumentError(KrecikException):
    message_schema = "No argument. Expected {expected}."
    attrs = {"expected": "not specified", "got": "not specified"}


class KrecikValueError(KrecikException):
    message_schema = "Invalid value for {type_name}: {value}."
    attrs = {"type_name": "not specified", "value": "not specified"}


class KrecikVariableRedeclarationError(KrecikException):
    message_schema = "Redeclaration of variable: {var_name} in function {func_name}."
    attrs = {"var_name": "not specified", "func_name": "not specified"}


class KrecikFunctionRedeclarationError(KrecikException):
    message_schema = "Redeclaration of function: {name}."
    attrs = {"name": "not specified"}


class KrecikVariableUndeclaredError(KrecikException):
    message_schema = "Undeclared variable: {name}."
    attrs = {"name": "not specified"}


class KrecikVariableUnassignedError(KrecikException):
    message_schema = "Usage of unassigned variable: {name}."
    attrs = {"name": "not specified"}


class KrecikVariableValueUnassignableError(KrecikException):
    message_schema = "Expression '{expr}' does not return value, thus cannot be assigned."
    attrs = {"expr": "not specified"}


class KrecikVariableAssignedTypeError(KrecikException):
    message_schema = "Cannot assign value type {val_type} to variable {name} of type {type}."
    attrs = {"val_type": "not specified", "name": "not specified", "type": "not specified"}


class KrecikIncompatibleTypesError(KrecikException):
    message_schema = "Unsupported operand {operand} for {type_1} and {type_2}."
    attrs = {"operand": "not specified", "type_1": "not specified", "type_2": "not specified"}


class UnsupportedOperationError(KrecikException):
    message_schema = (
        "Operation '{operation}' is unsupported for type '{type}'."
        "Expected one of: {expected_types}."
    )
    attrs = {
        "operation": "not specified",
        "type": "not specified",
        "expected_types": "not specified",
    }


class NullValueUsageError(KrecikException):
    message_schema = (
        "Expression {operand} of {operation} " "returns nothing thus cannot be used as operand."
    )
    attrs = {"operand": "not specified", "operation:": "not specified"}


class KrecikZeroDivisionError(KrecikException):
    message_schema = "Division by zero."
    attrs = {}


class ConditionTypeError(KrecikException):
    message_schema = "Condition must be of type logicki, got '{type}'."
    attrs = {"type": "not specified"}
