from antlr4 import CommonTokenStream, InputStream, RecognitionException
from antlr4.tree.Tree import ParseTreeWalker

from antlr.KrecikLexer import KrecikLexer
from antlr.KrecikListener import KrecikListener
from antlr.KrecikParser import KrecikParser
from antlr.KrecikVisitor import KrecikVisitor
from interpreter.exceptions import KrecikException, KrecikRecognitionError


class Interpreter:
    def __init__(
        self,
        lexer: KrecikLexer,
        parser: KrecikParser,
        listener: KrecikListener,
        walker: ParseTreeWalker,
        visitor: KrecikVisitor,
    ) -> None:
        self.lexer = lexer
        self.parser = parser
        self.listener = listener
        self.walker = walker
        self.visitor = visitor

    def interpret_file(self, file_path: str) -> None:
        with open(file_path, "r") as file:
            data = file.read()
        input_stream = InputStream(data)
        self.interpret_stream(input_stream)

    def interpret_stream(self, input_stream: InputStream) -> None:
        self.set_input(input_stream)
        pe_ctx = self.get_primary_expression_ctx()
        if pe_ctx is None or self.parser.getNumberOfSyntaxErrors() > 0:
            return
        self.walk_tree(pe_ctx)
        self.visit_tree(pe_ctx)

    def set_input(self, input_stream: InputStream) -> None:
        self.lexer.inputStream = input_stream
        token_stream = CommonTokenStream(self.lexer)
        self.parser.setTokenStream(token_stream)

    def get_primary_expression_ctx(self) -> KrecikParser.Primary_expressionContext | None:
        try:
            return self.parser.primary_expression()
        except RecognitionException as exc:
            krecik_exc = KrecikRecognitionError(extra_info=str(exc))
            self._handle_exception(krecik_exc)
            return None

    def walk_tree(self, ctx: KrecikParser.Primary_expressionContext) -> None:
        try:
            self.walker.walk(self.listener, ctx)
        except KrecikException as exc:
            self._handle_exception(exc)

    def visit_tree(self, ctx: KrecikParser.Primary_expressionContext) -> None:
        try:
            self.visitor.visit(ctx)
        except KrecikException as exc:
            self._handle_exception(exc)

    @staticmethod
    def _handle_exception(exc: KrecikException) -> None:
        print(exc)
