from pathlib import Path

from interpreter.exceptions import KrecikVariableRedeclarationError, KrecikVariableUndeclaredError, \
    KrecikVariableUnassignedError, KrecikVariableAssigningNoneValueError, KrecikVariableDifferentTypeAssignedError
from interpreter.interpreter import Interpreter
from interpreter.visitor import Visitor


class TestVariables:
    inputs_path = Path(__file__).parent.resolve() / "inputs"

    def test_variable_redeclared(self, visitor: Visitor) -> None:
        interpreter = Interpreter(visitor)
        input_path = str(self.inputs_path / "test_variable_redeclared.krecik")
        try:
            interpreter.interpret_file(input_path)
            assert False
        except KrecikVariableRedeclarationError:
            assert True
        except:
            assert False

    def test_variable_undeclared(self, visitor: Visitor) -> None:
        interpreter = Interpreter(visitor)
        input_path = str(self.inputs_path / "test_variable_undeclared.krecik")
        try:
            interpreter.interpret_file(input_path)
            assert False
        except KrecikVariableUndeclaredError:
            assert True
        except:
            assert False

    def test_variable_unassigned(self, visitor: Visitor) -> None:
        interpreter = Interpreter(visitor)
        input_path = str(self.inputs_path / "test_variable_unassigned.krecik")
        try:
            interpreter.interpret_file(input_path)
            assert False
        except KrecikVariableUnassignedError:
            assert True
        except:
            assert False

    def test_variable_assigning_none_value(self, visitor: Visitor) -> None:
        interpreter = Interpreter(visitor)
        input_path = str(self.inputs_path / "test_variable_assigning_none_value.krecik")
        try:
            interpreter.interpret_file(input_path)
            assert False
        except KrecikVariableAssigningNoneValueError:
            assert True
        except:
            assert False

    def test_variable_different_type_assigned(self, visitor: Visitor) -> None:
        interpreter = Interpreter(visitor)
        input_path = str(self.inputs_path / "test_variable_different_type_assigned.krecik")
        try:
            interpreter.interpret_file(input_path)
            assert False
        except KrecikVariableDifferentTypeAssignedError:
            assert True
        except:
            assert False

    def test_variable_ok(self, visitor: Visitor) -> None:
        interpreter = Interpreter(visitor)
        input_path = str(self.inputs_path / "test_variable_ok.krecik")
        try:
            interpreter.interpret_file(input_path)
            assert True
        except:
            assert False
