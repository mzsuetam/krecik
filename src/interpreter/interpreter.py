from typing import Any

from antlr4 import CommonTokenStream, InputStream  # type: ignore
from antlr4.error.Errors import RecognitionException  # type: ignore
from antlr4.tree.Tree import Tree  # type: ignore

from antlr.KrecikLexer import KrecikLexer
from antlr.KrecikParser import KrecikParser
from interpreter.exceptions import KrecikException
from interpreter.visitor import Visitor


class Interpreter:

    def __init__(self, visitor: Visitor) -> None:
        self.visitor = visitor

    def interpret_file(self, file_path: str) -> None:
        with open(file_path, "r") as file:
            data = file.read()
        input_stream = InputStream(data)
        self.interpret_data(input_stream)

    def interpret_data(self, input_stream: InputStream) -> None:
        parser_tree = self.parse_tree(input_stream)
        if parser_tree:
            self.visit_tree(parser_tree)

    def parse_tree(self, input_stream: InputStream) -> Tree | None:
        try:
            lexer = KrecikLexer(input_stream)
            stream = CommonTokenStream(lexer)
            parser = self.get_parser(stream)
            tree = parser.primary_expression()
            return tree
        except RecognitionException as exc:
            print(exc)
            return None

    @staticmethod
    def get_parser(stream: CommonTokenStream) -> KrecikParser:
        parser = KrecikParser(stream)
        parser.removeErrorListeners()
        # parser.addErrorListener()
        return parser

    def visit_tree(self, parser_tree: Tree) -> Any:
        try:
            return self.visitor.visit(parser_tree)
        except KrecikException as exc:
            print(exc)
            return
