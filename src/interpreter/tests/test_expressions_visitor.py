from typing import Callable

import pytest

from antlr.KrecikParser import KrecikParser
from interpreter.exceptions import (
    KrecikIncompatibleTypesError,
    KrecikZeroDivisionError,
)
from interpreter.krecik_types.cely import Cely
from interpreter.krecik_types.cislo import Cislo
from interpreter.krecik_types.krecik_type import KrecikType
from interpreter.krecik_types.logicki import KRECIK_FALSE, KRECIK_TRUE
from interpreter.visitors.visitor import Visitor


@pytest.mark.parametrize(
    ("input_string", "expected_result"),
    [
        ("2", Cely(2)),
        ("2 + 5 * 7", Cely(37)),
        ("2 * 5 - 7", Cely(3)),
        ("0 * 190", Cely(0)),
        ("100 / 30", Cely(3)),
        ("2. * 2.", Cislo(4.0)),
        ("2. * 2", Cislo(4.0)),
        ("0. * 190", Cislo(0.0)),
        ("100. / 30", Cislo(100 / 30)),
        ("100. - 7 / (5 + 2)", Cislo(99.0)),
        ("100 wetsi 10 oba true", KRECIK_TRUE),
        ("1 wetsi 2", KRECIK_FALSE),
        ("1 mensi 2", KRECIK_TRUE),
        ("2. wetsi 2", KRECIK_FALSE),
        ("2 mensi 2.", KRECIK_FALSE),
        ("2 wetsi 1.", KRECIK_TRUE),
        ("2. mensi 1.", KRECIK_FALSE),
        ("2 je 2", KRECIK_TRUE),
        ("2. je 2", KRECIK_TRUE),
        ("2 je 2.", KRECIK_TRUE),
        ("2. je 2.", KRECIK_TRUE),
        ("2 je 1", KRECIK_FALSE),
        ("2. je 1", KRECIK_FALSE),
        ("2 je 1.", KRECIK_FALSE),
        ("2. je 1.", KRECIK_FALSE),
        ("2 neje 2.1", KRECIK_TRUE),
        ("2. neje 2.1", KRECIK_TRUE),
        ("2 neje 2.0", KRECIK_FALSE),
        ("2. neje 2.0", KRECIK_FALSE),
        ("2 neje 2", KRECIK_FALSE),
        ("true je true", KRECIK_TRUE),
        ("true je false", KRECIK_FALSE),
        ("false je true", KRECIK_FALSE),
        ("false je false", KRECIK_TRUE),
        ("true neje true", KRECIK_FALSE),
        ("true neje false", KRECIK_TRUE),
        ("false neje true", KRECIK_TRUE),
        ("false neje false", KRECIK_FALSE),
        ("true", KRECIK_TRUE),
        ("false", KRECIK_FALSE),
        ("true oba false nebo true", KRECIK_FALSE),
        ("true nebo false oba false", KRECIK_TRUE),
        ("(true nebo false) oba true", KRECIK_TRUE),
    ],
)
def test_visit_expression(
    input_string: str,
    expected_result: KrecikType,
    get_parser_from_input: Callable[[str], KrecikParser],
    visitor: Visitor,
) -> None:
    parser = get_parser_from_input(input_string)
    expression_ctx = parser.expression()

    result = visitor.visit(expression_ctx)
    assert result == expected_result


@pytest.mark.parametrize(
    "input_string",
    [
        "1 / 0",
        "1/0",
        "4 / 0",
        "1 / 0.",
        "1. / 0",
        "1. / 0.",
    ],
)
def test_visit_expression_divide_by_zero(
    input_string: str,
    get_parser_from_input: Callable[[str], KrecikParser],
    visitor: Visitor,
) -> None:
    parser = get_parser_from_input(input_string)
    expression_ctx = parser.expression()

    with pytest.raises(KrecikZeroDivisionError):
        visitor.visit(expression_ctx)


@pytest.mark.parametrize(
    "input_string",
    [
        "true wetsi 1",
        "1 je true",
        "(1 wetsi 1) + 1",
    ],
)
def test_visit_expression_incompatible_types(
    input_string: str,
    get_parser_from_input: Callable[[str], KrecikParser],
    visitor: Visitor,
) -> None:
    parser = get_parser_from_input(input_string)
    expression_ctx = parser.expression()

    with pytest.raises(KrecikIncompatibleTypesError):
        visitor.visit(expression_ctx)
