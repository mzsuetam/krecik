from unittest.mock import create_autospec

from board.board_manager import BoardManager
from interpreter.builtin_function_names import BuiltinFunctionName
from interpreter.function_mappers.builtin_function_mapper import BuiltinFunctionMapper


def test_builtin_function_names() -> None:
    builtin_function_mapper = BuiltinFunctionMapper(create_autospec(BoardManager))
    implemented = builtin_function_mapper.function_map.keys()
    expected = {name for name in BuiltinFunctionName}
    missing_builtin_function_names = expected - implemented
    assert not missing_builtin_function_names, missing_builtin_function_names
