
# python standard library
import logging
import threading
from abc import abstractmethod, ABCMeta

# this package
from tuna.infrastructure.constants import RED, BOLD, RESET


DOT_JOIN = "{0}.{1}"
RED_ERROR = "{red}{bold}{{error}}{reset}{red}{{message}}{reset}".format(red=RED,
                                                            bold=BOLD,
                                                            reset=RESET)



class BaseClass(object):
    """
    This class holds the minimum common features.
    """
    def __init__(self):        
        self._logger = None
        return

    @property
    def logger(self):
        """
        :return: A logging object.
        """
        if self._logger is None:
            self._logger = logging.getLogger(DOT_JOIN.format(self.__module__,
                                  self.__class__.__name__))
        return self._logger

    def log_error(self, error, message=''):
        """
        Logs the error in bold red

        :param:

         - `error`: error type (prefix in red and bold)
         - `message`: descriptive message (red but not bold)
        """
        self.logger.error(RED_ERROR.format(error=error,
                                           message=message))
        return
        
# end BaseClass


class BaseThreadClass(BaseClass):
    """
    Extends the base-class with a run_thread method that will log tracebacks on exceptions.

    This is meant to log errors that kill threads.
    """
    __metaclass__ = ABCMeta
    def __init__(self):
        super(BaseThreadClass, self).__init__()
        self._logger = None
        self._thread = None
        return

    @property
    def thread(self):
        """
        This passes no arguments to run_thread -- override if needed
        
        :return: threading.Thread with self.run_thread as target and daemon True
        """
        if self._thread is None:
            self._thread = threading.Thread(target=self.run_thread)
            self._thread.daemon = True
        return self._thread

    def run_thread(self, *args, **kwargs):
        """
        catches any exceptions raised and logs them 
        
        :param: Whatever self.run accepts
        :precondition: self.run method exists and is thread-safe
        """
        try:
            self.run(*args, **kwargs)
        except Exception as error:
            import traceback
            self.logger.debug(traceback.format_exc())
            self.logger.error(error)
        return

    def reset(self):
        """
        Sets the thread to None
        """
        self._thread = None
        return

    @abstractmethod
    def run(self):
        """
        an abstract method called by the run_thread() method
        """
        return
# end BaseThreadClass
