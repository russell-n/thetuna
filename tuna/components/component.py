
# python standard library
from abc import abstractmethod, ABCMeta
import inspect
import os

# this package
from tuna import BaseClass
from tuna import TunaError

from tuna import RESET
from tuna import BOLD
from tuna.infrastructure.crash_handler import try_except
from tuna import ConfigurationError
from tuna.parts.countdown.countdown import TimeTracker


DOCUMENT_THIS = __name__ == '__builtin__'


class BaseComponent(BaseClass):
    """
    A base-class for Composite and Leaf
    """
    __metaclass__ = ABCMeta
    def __init__(self):
        """
        BaseComponent Constructor
        """
        super(BaseComponent, self).__init__()
        self._logger = None
        return

    @abstractmethod
    def __call__(self):
        """
        abstractmethod that will be the main invocation when implememented
        """
        return

    @abstractmethod
    def check_rep(self):
        """
        abstract: Representation-check called by composite

        :raise: ConfigurationError if representation invalid
        """
        return

    @abstractmethod
    def close(self):
        """
        abstractmethod: called for Keyboard Interrupts to allow file-closing
        """
        return        
