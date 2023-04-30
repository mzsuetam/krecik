from typing import Callable
from unittest.mock import create_autospec

import pytest
from antlr4 import ParseTreeWalker, TokenStream

from interpreter.function_mapper import FunctionMapper
from interpreter.interpreter import Interpreter
from interpreter.listener import Listener
from interpreter.recognizers.lexer import CustomLexer
from interpreter.recognizers.parser import CustomParser
from interpreter.variable_stack import VariableStack
from interpreter.visitors.visitor import Visitor


@pytest.mark.parametrize(
    "file_name",
    [
        # "incorrect.krecik",
        "simple.krecik",
        "test.krecik",
        "test2.krecik",
        "test3.krecik",
        "testVariables.krecik",
    ],
)
def test_interpret_file(
    file_name: str,
    get_input_path: Callable[[str], str],
) -> None:
    variable_stack = VariableStack()
    interpreter = Interpreter(
        CustomLexer(),
        CustomParser(TokenStream()),
        Listener(variable_stack),
        ParseTreeWalker(),
        Visitor(
            create_autospec(FunctionMapper),
            variable_stack,
        ),
        debug=True,
    )
    input_path = get_input_path(file_name)
    interpreter.interpret_file(input_path)
