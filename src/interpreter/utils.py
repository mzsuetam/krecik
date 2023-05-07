from interpreter.exceptions import (
    IncorrectArgumentsNumberError,
    IncorrectArgumentTypeError,
    NullArgumentError,
)
from interpreter.krecik_types.krecik_type import KrecikType


def validate_args(
    args: list[KrecikType],
    expected_args_types: list[type[KrecikType]],
) -> None:
    if len(args) != len(expected_args_types):
        raise IncorrectArgumentsNumberError(
            expected=len(expected_args_types),
            got=len(args),
        )
    parsed_args = []
    for arg, expected_arg_type in zip(args, expected_args_types):
        if isinstance(arg, expected_arg_type):
            parsed_args.append(arg)
            continue
        if arg is not None:
            raise IncorrectArgumentTypeError(
                expected=expected_arg_type.type_name,
                got=arg.type_name,
            )
        else:
            raise NullArgumentError(expected=expected_arg_type.type_name)
