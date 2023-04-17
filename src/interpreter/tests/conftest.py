import pytest

from board.board_manager import BoardManager
from board.tests.board_examples import plains
from display.board_publisher import BoardPublisher
from display.terminal_display import TerminalDisplay
from interpreter.function_mapper import FunctionMapper
from interpreter.variable_stack import VariableStack
from interpreter.visitor import Visitor


@pytest.fixture()
def visitor() -> Visitor:
    board = plains(6, 6)
    board_publisher = BoardPublisher()
    board_manager = BoardManager(board, board_publisher)

    window = TerminalDisplay(board)
    board_publisher.subscribe(window)

    function_mapper = FunctionMapper(board_manager)
    variable_stack = VariableStack()
    visitor = Visitor(function_mapper, variable_stack)
    return visitor
