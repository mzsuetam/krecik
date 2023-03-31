class KrecikException(Exception):
    message = "Error occurred."

    def __str__(self) -> str:
        return self.message


class NotDefinedFunctionError(KrecikException):
    message = "Function is not defined."


class IncorrectArgumentsNumberError(KrecikException):
    message = "Incorrect number of arguments."


class IncorrectArgumentTypeError(KrecikException):
    message = "Incorrect argument type."
