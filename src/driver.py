from argparse import ArgumentParser
from pathlib import Path

from antlr4 import ParseTreeWalker, TokenStream

from board.tests.board_examples import plains
from board.board_manager import BoardManager
from display.board_publisher import BoardPublisher
from interpreter.function_mapper import FunctionMapper
from interpreter.interpreter import Interpreter
from interpreter.lexer import CustomLexer
from interpreter.listener import Listener
from interpreter.parser import CustomParser
from interpreter.variable_stack import VariableStack
from interpreter.visitor import Visitor
from display.window import Window


def main(file_path: str, debug: bool) -> None:
    # board segment
    board = plains(10, 10)
    board_publisher = BoardPublisher()
    board_manager = BoardManager(board, board_publisher)

    # display segment
    window = Window(board)
    board_publisher.subscribe(window)

    # interpreter segment
    function_mapper = FunctionMapper(board_manager)
    variable_stack = VariableStack()
    interpreter = Interpreter(
        CustomLexer(),
        CustomParser(TokenStream()),
        Listener(variable_stack),
        ParseTreeWalker(),
        Visitor(function_mapper, variable_stack, debug=debug),
        debug=debug,
    )

    # running interpreter
    interpreter.interpret_file(file_path)


if __name__ == "__main__":
    """
    Runs interpreter on given file from /src/ directory.

    Example usages:
    $ python driver.py
    $ python driver.py --debug true
    $ python driver.py ./example_programs/example1.krecik
    $ python driver.py ./example_programs/example2.krecik --debug true
    """

    parser = ArgumentParser()
    parser.add_argument(
        "source",
        metavar="source file name",
        type=str,
        nargs="?",
        default="./example_programs/presentation.krecik",
    )
    parser.add_argument(
        "--debug",
        metavar="is debug mode",
        type=bool,
        nargs="?",
        default=False,
    )

    args = parser.parse_args()
    source_file_path = Path(__file__).parent / args.source
    main(file_path=str(source_file_path), debug=args.debug)
