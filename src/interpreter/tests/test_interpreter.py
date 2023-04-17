from pathlib import Path

from interpreter.interpreter import Interpreter
from interpreter.visitor import Visitor


class TestInterpreter:
    inputs_path = Path(__file__).parent.resolve() / "inputs"

    def test_interpreter(self, visitor: Visitor) -> None:
        interpreter = Interpreter(visitor)
        input_path = str(self.inputs_path / "simple.krecik")
        interpreter.interpret_file(input_path)
