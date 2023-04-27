from typing import Callable, Type

import pytest
from antlr.KrecikParser import KrecikParser
from interpreter.krecik_types.cely import Cely
from interpreter.krecik_types.cislo import Cislo
from interpreter.krecik_types.krecik_type import KrecikType
from interpreter.krecik_types.logicki import Logicki
from interpreter.visitor import Visitor


@pytest.mark.parametrize(
    ("input_string", "expected"),
    [
        ("cislo", Cislo),
        ("cely", Cely),
        ("logicki", Logicki),
    ],
)
def test_visit_var_type(
    input_string: str,
    expected: Type[KrecikType],
    get_parser_from_input: Callable[[str], KrecikParser],
    visitor: Visitor,
) -> None:
    parser = get_parser_from_input(input_string)
    var_type_ctx = parser.var_type()

    result = visitor.visitVar_type(var_type_ctx)
    assert result == expected


@pytest.mark.parametrize(
    "input_string",
    [
        "Cislo",
        "Cely",
        "Logicki",
        "dupa",
        "celyneczka",
    ],
)
def test_visit_var_type_incorrect(
    input_string: str,
    get_parser_from_input: Callable[[str], KrecikParser],
    visitor: Visitor,
) -> None:
    parser = get_parser_from_input(input_string)
    var_type_ctx = parser.var_type()

    with pytest.raises(NotImplementedError):
        visitor.visitVar_type(var_type_ctx)


@pytest.mark.parametrize(
    ("input_string", "expected_var_type", "expected_name"),
    [
        ("cislo a", Cislo, "a"),
        ("cely a", Cely, "a"),
        ("logicki jpdrugigmd", Logicki, "jpdrugigmd"),
    ],
)
def test_visit_declaration(
    input_string: str,
    expected_var_type: Type[KrecikType],
    expected_name: str,
    get_parser_from_input: Callable[[str], KrecikParser],
    visitor: Visitor,
) -> None:
    parser = get_parser_from_input(input_string)
    declaration_ctx = parser.declaration()

    visitor.visitDeclaration(declaration_ctx)
    visitor.variable_stack.declare_variable.assert_called_once_with(  # type: ignore[attr-defined]
        expected_var_type, expected_name
    )
