from tuna.infrastructure.baseclass import BaseClass

# some constants
TUNASECTION = "TUNA"
MODULES_SECTION = 'MODULES'
VERSION = "2014.06.12"
FILE_TIMESTAMP = "%Y_%m_%d_%I:%M:%S_%p"
BLUE = "\033[34m"
RED  = "\033[31m"
BOLD = "\033[1m"
RESET = "\033[0;0m"
NEWLINE = '\n'

class TunaError(Exception):
    """
    An exception for the top-level code (catch all predictable errors)
    """

class ConfigurationError(TunaError):
    """
    An Error for configuration problems
    """

class DontCatchError(TunaError):
    """
    A sibling to the configuration error that should crash the program if raised
    """
