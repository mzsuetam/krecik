from antlr4 import CommonTokenStream, InputStream
from antlr4.error.Errors import ParseCancellationException

from antlr.KrecikLexer import KrecikLexer
from antlr.KrecikParser import KrecikParser
from board.board import Board
from window.window import Window
from .visitor import Visitor


class Interpreter:
    def __init__(self) -> None:
        self.board: Board | None = None
        self.window: Window | None = None

    def set_board(self, board: Board) -> None:
        self.board = board
        self.window = Window(board)

    def interpret(self, file_path: str) -> None:
        if self.board is None:
            raise RuntimeError("Must specify board before interpreting.")
        with open(file_path, "r") as file:
            data = InputStream(file.read())
        try:
            lexer = KrecikLexer(data)
            stream = CommonTokenStream(lexer)
            parser = KrecikParser(stream)
            tree = parser.primary_expression()
        except ParseCancellationException as exc:
            print(exc)
            return
        visitor = Visitor(self.board, self.window)
        return visitor.visit(tree)
