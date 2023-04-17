from argparse import ArgumentParser

from board.tests.board_examples import plains
from board.board_manager import BoardManager
from display.board_publisher import BoardPublisher
from interpreter.function_mapper import FunctionMapper
from interpreter.interpreter import Interpreter
from interpreter.variable_stack import VariableStack
from interpreter.visitor import Visitor
from display.window import Window


def main(file_path: str) -> None:

    board = plains(6, 4)
    board_publisher = BoardPublisher()
    board_manager = BoardManager(board, board_publisher)

    window = Window(board)
    board_publisher.subscribe(window)

    function_mapper = FunctionMapper(board_manager)
    variable_stack = VariableStack()
    visitor = Visitor(function_mapper, variable_stack)
    interpreter = Interpreter(visitor)
    interpreter.interpret_file(file_path)


if __name__ == "__main__":
    """
    Example usage:
    $ python src/driver.py src/interpreter/tests/inputs/test.krecik
    """

    parser = ArgumentParser()
    parser.add_argument("source_file_path", metavar="source", type=str, nargs=1)
    args = parser.parse_args()
    main(args.source_file_path[0])
