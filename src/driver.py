from argparse import ArgumentParser
from pathlib import Path

from antlr4 import ParseTreeWalker, TokenStream

from board.board_manager import BoardManager
from board.tests.board_examples import jebus_cross, plains, random
from display.board_publisher import BoardPublisher
from display.terminal_display import TerminalDisplay
from display.window import Window
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


def main(
    width: int,
    height: int,
    board_type: str,
    file_path: str,
    allow_prints: bool,
    print_stacktraces: bool,
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
    builtin_function_mapper = BuiltinFunctionMapper(board_manager)
    declared_function_mapper = DeclaredFunctionMapper()
    variable_stack = VariableStack()
    interpreter = Interpreter(
        CustomLexer(),
        CustomParser(TokenStream()),
        Listener(declared_function_mapper, variable_stack),
        ParseTreeWalker(),
        Visitor(builtin_function_mapper, declared_function_mapper, variable_stack, allow_prints),
        print_stacktraces,
    )

    # running interpreter
    file_path = file_path if file_path.endswith(".krecik") else file_path + ".krecik"
    interpreter.interpret_file(file_path)


if __name__ == "__main__":
    """
    Runs interpreter on given file from /src/ directory.

    Example usages:
    $ python driver.py
    $ python driver.py ./example_programs/example1.krecik
    $ python driver.py ./example_programs/example1
    $ python driver.py ./example_programs/example1 --width 12 --height 12 --board-type random
    $ python driver.py ./example_programs/example1 --display window
    $ python driver.py ./example_programs/example2 --allow-prints true
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
        "--allow-prints",
        metavar="is prints allowed in code",
        type=bool,
        nargs="?",
        default=False,
    )
    parser.add_argument(
        "--print-stacktraces",
        metavar="should stacktraces be printed in python convention",
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
        allow_prints=args.allow_prints,
        print_stacktraces=args.print_stacktraces,
        display=args.display,
    )
