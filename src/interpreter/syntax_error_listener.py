from antlr4 import RecognitionException  # type: ignore
from antlr4.Recognizer import Recognizer  # type: ignore
from antlr4.Token import CommonToken  # type: ignore
from antlr4.error.ErrorListener import ErrorListener  # type: ignore

from interpreter.exceptions import KrecikSyntaxError


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
