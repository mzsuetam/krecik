from argparse import ArgumentParser
from pathlib import Path

from antlr4 import ParseTreeWalker, TokenStream

from board.tests.board_examples import jebus_cross, plains, random
from board.board_manager import BoardManager
from display.board_publisher import BoardPublisher
from display.terminal_display import TerminalDisplay
from interpreter.function_mapper import FunctionMapper
from interpreter.interpreter import Interpreter
from interpreter.lexer import CustomLexer
from interpreter.listener import Listener
from interpreter.parser import CustomParser
from interpreter.variable_stack import VariableStack
from interpreter.visitor import Visitor
from display.window import Window


def main(
    width: int,
    height: int,
    board_type: str,
    file_path: str,
    debug: bool,
    display: str,
) -> None:
    # board segment
    board_mapping = {
        "plains": plains,
        "random": random,
        "cross": jebus_cross,
    }
    board_generator = board_mapping.get(board_type, plains)
    board = board_generator(width, height)
    board_publisher = BoardPublisher()
    board_manager = BoardManager(board, board_publisher)

    # display segment
    if display in {"window", "both"}:
        window = Window(board)
        board_publisher.subscribe(window)
    if display in {"terminal", "both"}:
        terminal = TerminalDisplay(board)
        board_publisher.subscribe(terminal)

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
    $ python driver.py ./example_programs/example1.krecik
    $ python driver.py ./example_programs/example1.krecik --width 12 --height 12 --board-type random
    $ python driver.py ./example_programs/example1.krecik --display window
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
        "--width",
        metavar="width of the board",
        type=int,
        nargs="?",
        default=8,
    )
    parser.add_argument(
        "--height",
        metavar="height of the board",
        type=int,
        nargs="?",
        default=8,
    )
    parser.add_argument(
        "--board-type",
        metavar="type of the board",
        type=str,
        nargs="?",
        default="plains",
    )
    parser.add_argument(
        "--debug",
        metavar="is debug mode",
        type=bool,
        nargs="?",
        default=False,
    )
    parser.add_argument(
        "--display",
        metavar="type of display",
        type=str,
        nargs="?",
        default="both",
    )

    args = parser.parse_args()
    source_file_path = Path(__file__).parent / args.source
    main(
        width=args.width,
        height=args.height,
        board_type=args.board_type,
        file_path=str(source_file_path),
        debug=args.debug,
        display=args.display,
    )
