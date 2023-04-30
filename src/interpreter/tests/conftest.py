from pathlib import Path
from typing import Callable
from unittest.mock import create_autospec

import pytest
from antlr4 import CommonTokenStream, InputStream

from antlr.KrecikParser import KrecikParser
from interpreter.function_mapper import FunctionMapper
from interpreter.recognizers.lexer import CustomLexer
from interpreter.recognizers.parser import CustomParser
from interpreter.variable_stack import VariableStack
from interpreter.visitors.visitor import Visitor


@pytest.fixture()
def visitor() -> Visitor:
    function_mapper = create_autospec(FunctionMapper)
    variable_stack = create_autospec(VariableStack)
    visitor = Visitor(function_mapper, variable_stack)
    return visitor


@pytest.fixture()
def get_input_path() -> Callable[[str], str]:
    def _(source_file_name: str = "test.krecik") -> str:
        return str(Path(__file__).parent / "inputs" / source_file_name)

    return _


@pytest.fixture()
def get_parser_from_input() -> Callable[[str], KrecikParser]:
    def _(input_string: str) -> KrecikParser:
        input_stream = InputStream(input_string)
        lexer = CustomLexer(input_stream)
        token_stream = CommonTokenStream(lexer)
        return CustomParser(token_stream)

    return _
