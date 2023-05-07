from typing import Callable
from unittest.mock import create_autospec

import pytest
from antlr4 import ParseTreeWalker, TokenStream

from interpreter.function_mappers.builtin_function_mapper import (
    BuiltinFunctionMapper,
)
from interpreter.function_mappers.declared_function_mapper import DeclaredFunctionMapper
from interpreter.interpreter import Interpreter
from interpreter.listener import Listener
from interpreter.recognizers.lexer import CustomLexer
from interpreter.recognizers.parser import CustomParser
from interpreter.variable_stack import VariableStack
from interpreter.visitors.visitor import Visitor


@pytest.mark.parametrize(
    "file_name",
    [
        "loop.krecik",
        "simple.krecik",
        "test.krecik",
        "test2.krecik",
        "test3.krecik",
        "test_variables.krecik",
    ],
)
def test_interpret_file(
    file_name: str,
    get_input_path: Callable[[str], str],
) -> None:
    variable_stack = VariableStack()
    declared_function_mapper = DeclaredFunctionMapper()
    interpreter = Interpreter(
        CustomLexer(),
        CustomParser(TokenStream()),
        Listener(declared_function_mapper, variable_stack),
        ParseTreeWalker(),
        Visitor(
            create_autospec(BuiltinFunctionMapper),
            declared_function_mapper,
            variable_stack,
            allow_prints=True,
        ),
        print_stacktraces=True,
    )
    input_path = get_input_path(file_name)
    interpreter.interpret_file(input_path)
