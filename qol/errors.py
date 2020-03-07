"""
    Module containing custom error classes for the package.
"""

class QolError(Exception):
    """ Base error class for the QOL package. """


class MissingParameterError(QolError):
    """ Raised when a parameter is missing from the input. """

    def __init__(self, parameterNm, *args, **kwargs):
        """
        Parameters
        ----------
        parameterNm: str
            Name of the parameters group with missing parameters.
        *args: positional arguments
            All the parameters missing from the group.
        **kwargs: keyword arguments
            Passed to the QolError init.
        """
        # Create message
        if len(args) == 0:
            return
        elif len(args) > 1:
            missing = "', '".join(args[:-1])
            missing = f"'{missing}' and '{args[-1]}'"
        else:
            missing = f"'{args[0]}'"
        msg = f"Parameters group: {parameterNm} is missing {missing}."
        print(msg)
        super().__init__(msg, *args, **kwargs)


class IncorrectParameterError(QolError):
    """ Raised when parameter given is an unaccepted value. """

    def __init__(self, value, parameter=None, expected=None, **kwargs):
        """
        Parameters
        ----------
        value:
            Value given to the parameter that is not accepted.
        parameter: str, optional
            Name of the parameter the that received the unexpected value.
        expected: list-like or str, optional
            The values that the `parameter` expects.
        **kwargs: keyword arguments
            Passed to QolError init.
        """
        # Create message
        msg = f"Incorrect value of {value}"
        if not parameter is None:
            msg += f" for parameter {parameter}"
        if not expected is None:
            msg += f" expected value(s) {expected}"
        super().__init__(msg, **kwargs)
