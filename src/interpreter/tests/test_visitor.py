from typing import Callable

import pytest
from pytest_mock import MockFixture

from antlr.KrecikParser import KrecikParser
from interpreter.exceptions import KrecikVariableAssignedTypeError
from interpreter.krecik_types.cely import Cely
from interpreter.krecik_types.cislo import Cislo
from interpreter.krecik_types.krecik_type import KrecikType
from interpreter.krecik_types.logicki import KRECIK_FALSE, KRECIK_TRUE, Logicki
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
    expected: type[KrecikType],
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
    expected_var_type: type[KrecikType],
    expected_name: str,
    get_parser_from_input: Callable[[str], KrecikParser],
    visitor: Visitor,
) -> None:
    parser = get_parser_from_input(input_string)
    declaration_ctx = parser.declaration()

    visitor.visit(declaration_ctx)
    visitor.variable_stack.declare_variable.assert_called_once_with(  # type: ignore[attr-defined]
        expected_var_type,
        expected_name,
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
    visitor.variable_stack.get_var.return_value = value_from_stack  # type: ignore[attr-defined]

    visitor.visit(assignment_ctx)
    visitor.variable_stack.get_var.assert_called_once()  # type: ignore[attr-defined]
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
    visitor.variable_stack.declare_variable.return_value = (  # type: ignore[attr-defined]
        value_from_stack
    )

    visitor.visit(assignment_ctx)
    visitor.variable_stack.declare_variable.assert_called_once()  # type: ignore[attr-defined]
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
    visitor.variable_stack.get_var.return_value = value_from_stack  # type: ignore[attr-defined]
    visitor.variable_stack.declare_variable.return_value = (  # type: ignore[attr-defined]
        value_from_stack
    )

    with pytest.raises(KrecikVariableAssignedTypeError):
        visitor.visit(assignment_ctx)


@pytest.mark.parametrize(
    ("input_string", "dupa_value", "expected_body_number"),
    [
        pytest.param("kdyz (dupa) {}", KRECIK_TRUE, 0, id="condition met"),
        pytest.param("kdyz (dupa) {}", KRECIK_FALSE, None, id="condition not met"),
        pytest.param("kdyz (dupa) {} jiny {}", KRECIK_TRUE, 0, id="condition met with else"),
        pytest.param("kdyz (dupa) {} jiny {}", KRECIK_FALSE, 1, id="condition not met with else"),
    ],
)
def test_visit_conditional_instruction(
    input_string: str,
    dupa_value: KrecikType,
    expected_body_number: int | None,
    get_parser_from_input: Callable[[str], KrecikParser],
    visitor: Visitor,
    mocker: MockFixture,
) -> None:
    parser = get_parser_from_input(input_string)
    cond_instruction_ctx = parser.conditional_instruction()
    visitor.variable_stack.get_var.side_effect = [dupa_value]  # type: ignore[attr-defined]
    visit_body_mock = mocker.patch("interpreter.visitors.visitor.Visitor.visitBody")

    visitor.visit(cond_instruction_ctx)
    if expected_body_number is None:
        visit_body_mock.assert_not_called()
    else:
        expected_call_arg = cond_instruction_ctx.body(expected_body_number)
        visit_body_mock.assert_called_once_with(expected_call_arg)


@pytest.mark.parametrize(
    ("dupa_values", "expected_call_number"),
    [
        pytest.param(
            [KRECIK_FALSE],
            0,
            id="simple condition false",
        ),
        pytest.param(
            [KRECIK_TRUE, KRECIK_FALSE],
            1,
            id="dupa set to false after one repetition",
        ),
        pytest.param(
            [KRECIK_TRUE, KRECIK_TRUE, KRECIK_FALSE],
            2,
            id="dupa set to false after two repetitions",
        ),
        pytest.param(
            [KRECIK_TRUE, KRECIK_TRUE, KRECIK_TRUE, KRECIK_FALSE],
            3,
            id="dupa set to false after three repetitions",
        ),
    ],
)
def test_visit_loop_instruction(
    dupa_values: list[KrecikType],
    expected_call_number: int,
    get_parser_from_input: Callable[[str], KrecikParser],
    visitor: Visitor,
    mocker: MockFixture,
) -> None:
    parser = get_parser_from_input("opakujte (dupa) {}")
    loop_instruction_ctx = parser.loop_instruction()
    visitor.variable_stack.get_var.side_effect = dupa_values  # type: ignore[attr-defined]
    visit_body_mock = mocker.patch("interpreter.visitors.visitor.Visitor.visitBody")
    visitor.declared_function_mapper.is_returning.return_value = False  # type: ignore[attr-defined]

    visitor.visit(loop_instruction_ctx)
    assert visit_body_mock.call_count == expected_call_number
