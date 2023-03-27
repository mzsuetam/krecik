from pathlib import Path

import pytest

from board.board_examples import jebus_cross, plains
from interpreter.interpreter import Interpreter


def test_interpreter() -> None:
    interpreter = Interpreter()
    interpreter.set_board(plains(6, 6))
    input_path = str(Path(__file__).parent.parent.parent.resolve() / "inputs" / "simple.krecik")
    interpreter.interpret(input_path)


@pytest.mark.skip
def test_interpreter_jebus() -> None:
    interpreter = Interpreter()
    interpreter.set_board(jebus_cross())
    input_path = str(Path(__file__).parent.parent.parent.resolve() / "inputs" / "simple.krecik")
    interpreter.interpret(input_path)
