from typing import Any

from antlr4 import CommonTokenStream, InputStream
from antlr4.tree.Tree import ParseTree, ParseTreeWalker

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
        if parser_tree is None:
            return
        try:
            self.walk_tree(parser_tree)
            self.visit_tree(parser_tree)
        except KrecikException as exc:
            print(exc)
            return

    def get_tree(self, input_stream: InputStream) -> ParseTree | None:
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
    def parse_tree(parser: KrecikParser) -> ParseTree | None:
        tree = parser.primary_expression()
        if parser.getNumberOfSyntaxErrors() > 0:
            return None
        return tree

    def walk_tree(self, parser_tree: ParseTree) -> None:
        listener = Listener(self.visitor.variable_stack)
        walker = ParseTreeWalker()
        walker.walk(listener, parser_tree)

    def visit_tree(self, parser_tree: ParseTree) -> Any:
        self.visitor.visit(parser_tree)
