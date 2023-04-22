from typing import Any

from antlr4 import RecognitionException
from antlr4.Recognizer import Recognizer
from antlr4.Token import CommonToken
from antlr4.error.ErrorListener import ErrorListener

from interpreter.exceptions import KrecikSyntaxError


class RecognizerWithCustomListener(Recognizer):
    def __init__(self, *args: Any, **kwargs: Any) -> None:
        super().__init__()
        self.removeErrorListeners()
        listener = SyntaxErrorListener()
        self.addErrorListener(listener)


class SyntaxErrorListener(ErrorListener):
    def syntaxError(
        self,
        recognizer: Recognizer,
        offending_symbol: CommonToken,
        line: int,
        column: int,
        msg: str,
        e: RecognitionException,
    ) -> None:
        exc = KrecikSyntaxError(extra_info=msg)
        exc.start_line = line
        exc.stop_line = line
        exc.start_column = column
        exc.stop_column = column
        print(exc)
