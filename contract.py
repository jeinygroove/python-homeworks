"""This module contains decorator @contract that checks function types."""
from functools import wraps
from typing import Optional, Tuple, Type


class ContractError(Exception):
    """Error it raise when someone breaks our contract."""

    def __init__(self, message: str) -> None:
        """
        Initialize ContractError.

        Parameters:
            message: Error message, describing broken contract.
        """
        self.message = message
        super().__init__(self.message)


Any = object()
Void = type(None)


def _check_arg_types(arg_types, args):
    argument_check_type_array = [
        (arg_pos, type_and_arg[0], type_and_arg[1])
        for arg_pos, type_and_arg in enumerate(zip(arg_types, args))
    ]
    for arg_pos, arg_type, arg in argument_check_type_array:
        if arg_type is not Any and not isinstance(arg, arg_type):
            raise ContractError(
                'Argument {0} has wrong type'.format(
                    arg_pos + 1,
                ),
            ) from TypeError


def _check_return_type(return_type, return_result):
    if return_type is not None and not isinstance(return_result, return_type):
        raise ContractError('Wrong return type.') from TypeError


def contract(          # noqa: WPS231
    arg_types: Optional[Tuple[Type, ...]] = None,
    return_type: Optional[Type] = None,
    raises: Optional[Tuple[Type, ...]] = None,
):  # noqa: DAR401
    """
    Contains decorator that checks signature of function.

    If you don't want to check some type, use `Any` instead.

    Parameters:
        arg_types: Types of function arguments, None by default.
        return_type: Type of returned value, None by default.
        raises: Exception types which function can raise, None by default.

    Returns:
        return_result: Result that wrapped function should return.

    Raises:
        ContractError: if signature is not equal with described.
        raises: exceptions enumerated in raises.
    """

    def decorator(func): # noqa: 231
        @wraps(func)
        def wrapper(*args, **kwargs): # noqa: 231
            if arg_types is not None:
                if kwargs:
                    raise ContractError(
                        'Usage of keyworded arguments is forbidden.',
                    )
                if len(arg_types) != len(args):
                    raise ContractError('Incorrect number of parameters.')
                _check_arg_types(arg_types, args)

            if raises is None:
                return_result = func(*args, **kwargs)
            else:
                try:
                    return_result = func(*args, **kwargs)
                except raises:
                    raise
                except Exception as exc: # noqa: 239
                    raise ContractError(
                        "Exception that wasn't stated in 'raises'.",
                    ) from exc

            _check_return_type(return_type, return_result)
            return return_result

        return wrapper

    return decorator
