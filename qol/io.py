"""
    Module containing convient functions/classes for some standard inputs
    and outputs, such as reading/writing parameters files.
"""

##### IMPORTS #####
# Standard imports
import json

# Package imports
from .errors import MissingParameterError

##### Classes #####
class Parameters:
    """
        Class for reading and writing parameters to files in json format.
    """
    # Class constants
    _INDENT = 4

    # Default parameters
    DEFAULT_PARAMETERS = {}

    def __init__(self, path=None, parameters=None):
        """
            Initiate the class by reading file if given, using `parameters` if given
            or with defaults.

            Parameters
            ----------
            path: str, optional
                Path to parameters file, file should be json format.
            parameters: dict, optional
                Dictionary containing parameters.
        """
        if not path is None:
            self.read(path)
        elif not parameters is None:
            self._parameters = dict(parameters)
        else:
            self._parameters = self.DEFAULT_PARAMETERS
        return

    def read(self, path):
        """
            Read the parameters file given, using json module.

            Parameters
            ----------
            path: str
                Path to the parameters file, file should be json format.

            Returns
            -------
            params: dict
                Dictionary containing all the parameters read.
        """
        # Read parameters
        with open(path, 'rt') as f:
            self._parameters = json.load(f)

        return self._parameters

    def __str__(self):
        """
            Creates json string.

            Returns
            -------
            params: str
                Json str dump of parameters.
        """
        return json.dumps(self._parameters, indent=self._INDENT)

    def write(self, path):
        """
            Write parameters to file.

            Parameters
            ----------
            path: str
                Path to write parameter file to.

            Returns
            -------
                Nothing
        """
        # Write parameters to file
        with open(path, 'wt') as f:
            json.dump(self._parameters, f, indent=self._INDENT)
        return

    def checkParameters(self, expected, name=''):
        """ Checks if parameters contain expected values.

            Checks if the given parameters dictionary contains all the
            expected parameters, raises error if not.

            Parameters
            ----------
            expected: iterable
                List of the expected parameters, which refer to the
                keys of the parameters.
            name: str, optional
                Name of the parameter group being checked.

            Returns
            -------
            params: dict
                New dictionary containing only the expected
                parameters.

            Raises
            ------
            MissingParameterError
                If any of the expected parameters are not in the dictionary.
        """
        checkedParams = {}
        missing = []
        for i in expected:
            try:
                checkedParams[i] = self._parameters[i]
            except KeyError:
                missing.append(i)

        # Raise error if any are missing
        if len(missing) > 0:
            MissingParameterError(name, *missing)

        return checkedParams

    def get(self, parameter):
        """ Get a single parameter, from the object.

            Parameters
            ----------
            parameter: str
                Name of the parameter to retrieve.

            Returns
            -------
            parameter: type of parameter
                The value of the named parameter.

            Raises
            ------
            MissingParameterError
                If the parameter doesn't exist.
        """
        p = self.checkParameters((parameter,))
        return p[parameter]
