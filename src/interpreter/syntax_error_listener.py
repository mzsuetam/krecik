from typing import Any

from antlr4 import NoViableAltException, RecognitionException
from antlr4.Recognizer import Recognizer
from antlr4.Token import CommonToken
from antlr4.error.ErrorListener import ErrorListener
from antlr4.error.Errors import FailedPredicateException, InputMismatchException

from interpreter.exceptions import (
    KrecikException,
    KrecikFailedPredicateException,
    KrecikInputMismatchException,
    KrecikNoViableAltException,
    KrecikSyntaxError,
)


class RecognizerWithCustomListener(Recognizer):
    def __init__(self, *args: Any, **kwargs: Any) -> None:
        super().__init__()
        self.removeErrorListeners()
        listener = SyntaxErrorListener()
        self.addErrorListener(listener)


class SyntaxErrorListener(ErrorListener):
    def __init__(self) -> None:
        self.errors: list[KrecikException] = []

    def syntaxError(
        self,
        recognizer: Recognizer,
        offending_symbol: CommonToken,
        line: int,
        column: int,
        msg: str,
        e: RecognitionException,
    ) -> None:
        if e is None:  # for extraneous input error
            return
        exc: KrecikException
        if isinstance(e, NoViableAltException):
            exc = KrecikNoViableAltException(offending_symbol=offending_symbol.text)
        elif isinstance(e, InputMismatchException):
            exc = KrecikInputMismatchException(extra_info=msg)
        elif isinstance(e, FailedPredicateException):
            exc = KrecikFailedPredicateException(extra_info=msg)
        else:
            exc = KrecikSyntaxError(extra_info=msg)
        exc.start_line = line
        exc.stop_line = line
        exc.start_column = column
        exc.stop_column = column
        self.errors.append(exc)
