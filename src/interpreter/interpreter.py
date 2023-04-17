from typing import Any

from antlr4 import CommonTokenStream, InputStream  # type: ignore
from antlr4.error.Errors import RecognitionException  # type: ignore
from antlr4.tree.Tree import Tree, ParseTreeWalker  # type: ignore

from antlr.KrecikLexer import KrecikLexer
from antlr.KrecikParser import KrecikParser
from interpreter.exceptions import KrecikException
from interpreter.syntax_error_listener import SyntaxErrorListener
from interpreter.listener import Listener
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
        parser_tree = self.get_tree(input_stream)
        if parser_tree is not None:
            if self.walk(parser_tree):
                return
            self.visit_tree(parser_tree)

    def get_tree(self, input_stream: InputStream) -> Tree | None:
        lexer = KrecikLexer(input_stream)
        stream = CommonTokenStream(lexer)
        parser = self.get_parser(stream)
        return self.parse_tree(parser)

    @staticmethod
    def get_parser(stream: CommonTokenStream) -> KrecikParser:
        parser = KrecikParser(stream)
        parser.removeErrorListeners()
        parser.addErrorListener(SyntaxErrorListener())
        return parser

    @staticmethod
    def parse_tree(parser: KrecikParser) -> Tree | None:
        tree = parser.primary_expression()
        if parser.getNumberOfSyntaxErrors() > 0:
            return None
        return tree

    def visit_tree(self, parser_tree: Tree) -> Any:
        try:
            return self.visitor.visit(parser_tree)
        except KrecikException as exc:
            print(exc)
            return

    def walk(self, parser_tree: Tree) -> int | None:
        try:
            listener = Listener(self.visitor.variable_stack)
            walker = ParseTreeWalker()
            walker.walk(listener, parser_tree)
            return None
        except KrecikException as exc:
            print(exc)
            return -1
