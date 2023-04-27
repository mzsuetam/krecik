from typing import Callable
from unittest.mock import create_autospec

from antlr4 import ParseTreeWalker, TokenStream

from interpreter.function_mapper import FunctionMapper
from interpreter.interpreter import Interpreter
from interpreter.lexer import CustomLexer
from interpreter.listener import Listener
from interpreter.parser import CustomParser
from interpreter.variable_stack import VariableStack
from interpreter.visitor import Visitor


def test_interpret_file(get_input_path: Callable[[str], str]) -> None:
    variable_stack = VariableStack()
    interpreter = Interpreter(
        CustomLexer(),
        CustomParser(TokenStream()),
        Listener(create_autospec(FunctionMapper), variable_stack),
        ParseTreeWalker(),
        Visitor(
            create_autospec(FunctionMapper),
            variable_stack,
        ),
    )
    input_path = get_input_path("simple.krecik")
    interpreter.interpret_file(input_path)
