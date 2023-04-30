from typing import Callable, Type

import pytest

from antlr.KrecikParser import KrecikParser
from interpreter.exceptions import KrecikVariableAssignedTypeError
from interpreter.krecik_types.cely import Cely
from interpreter.krecik_types.cislo import Cislo
from interpreter.krecik_types.krecik_type import KrecikType
from interpreter.krecik_types.logicki import KRECIK_TRUE, Logicki
from interpreter.visitors.visitor import Visitor


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

    result = visitor.visit(var_type_ctx)
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
        visitor.visit(var_type_ctx)


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

    visitor.visit(declaration_ctx)
    visitor.variable_stack.declare.assert_called_once_with(  # type: ignore[attr-defined]
        expected_var_type, expected_name
    )


@pytest.mark.parametrize(
    ("input_string", "value_from_stack", "expected_value"),
    [
        ("a = 0.", Cislo(10.0), Cislo(0.0)),
        ("a = 0", Cely(8643), Cely(0)),
        ("chuj = true", Logicki(False), KRECIK_TRUE),
    ],
)
def test_visit_assignment(
    input_string: str,
    value_from_stack: KrecikType,
    expected_value: KrecikType,
    get_parser_from_input: Callable[[str], KrecikParser],
    visitor: Visitor,
) -> None:
    parser = get_parser_from_input(input_string)
    assignment_ctx = parser.assignment()
    visitor.variable_stack.get_var_value.return_value = (  # type: ignore[attr-defined]
        value_from_stack
    )

    visitor.visit(assignment_ctx)
    visitor.variable_stack.get_var_value.assert_called_once()  # type: ignore[attr-defined]
    assert value_from_stack == expected_value


@pytest.mark.parametrize(
    ("input_string", "value_from_stack", "expected_value"),
    [
        ("cislo a = 0.", Cislo(None), Cislo(0.0)),
        ("cely a = 0", Cely(None), Cely(0)),
        ("logicki chuj = true", Logicki(None), KRECIK_TRUE),
    ],
)
def test_visit_assignment_with_declaration(
    input_string: str,
    value_from_stack: KrecikType,
    expected_value: KrecikType,
    get_parser_from_input: Callable[[str], KrecikParser],
    visitor: Visitor,
) -> None:
    parser = get_parser_from_input(input_string)
    assignment_ctx = parser.assignment()
    visitor.variable_stack.declare.return_value = value_from_stack  # type: ignore[attr-defined]

    visitor.visit(assignment_ctx)
    visitor.variable_stack.declare.assert_called_once()  # type: ignore[attr-defined]
    assert value_from_stack == expected_value


@pytest.mark.parametrize(
    ("input_string", "value_from_stack"),
    [
        ("a = 0.", Cely(None)),
        ("cely a = 0.", Cely(None)),
        ("logicki chuj = 0", Logicki(None)),
    ],
)
def test_visit_assignment_incorrect_types(
    input_string: str,
    value_from_stack: KrecikType,
    get_parser_from_input: Callable[[str], KrecikParser],
    visitor: Visitor,
) -> None:
    parser = get_parser_from_input(input_string)
    assignment_ctx = parser.assignment()
    visitor.variable_stack.get_var_value.return_value = (  # type: ignore[attr-defined]
        value_from_stack
    )
    visitor.variable_stack.declare.return_value = value_from_stack  # type: ignore[attr-defined]

    with pytest.raises(KrecikVariableAssignedTypeError):
        visitor.visit(assignment_ctx)
