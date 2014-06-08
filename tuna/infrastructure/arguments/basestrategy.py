
# python standard library
from ConfigParser import NoSectionError
import datetime

# this package
from optimization import BaseClass

from optimization.infrastructure.crash_handler import try_except, log_error
from optimization import RED, BOLD, RESET
from optimization.infrastructure.quartermaster import QuarterMaster


RED_ERROR = "{red}{bold}{{error}}{reset}".format(red=RED,
                                                 bold=BOLD,
                                                 reset=RESET)
INFO_STRING = '{b}**** {{0}} ****{r}'.format(b=BOLD, r=RESET)


DOCUMENT_THIS = __name__ == '__builtin__'


class BaseStrategy(BaseClass):
    """
    A base for the sub-commands
    """
    def __init__(self):
        """
        BaseStrategy Constructor
        """
        super(BaseStrategy, self).__init__()
        self._logger = None
        self.error = (Exception, KeyboardInterrupt)
        self.error_message = "Oops, I Crapped My Pants"
        self.optimizer = None
        return

    quartermaster = QuarterMaster()

    def build_optimizer(self, configfiles):
        """
        Tries to build the optimization plugin
        (has a side-effect of setting self.optimizer so that crash-handling can get to it)

        :return: optimizer or None
        :postcondition: self.optimizer set to optimizer (or None on failure)

        :param: `configfiles`: a list of configuration files for the optimizer
        """
        plugin = self.quartermaster.get_plugin('Optimizer')
        
        # The optimizer needs the config-filenames
        try:
            self.optimizer = plugin(configfiles=configfiles).product
        except NoSectionError as error:
            self.logger.error(error)
            self.logger.error(RED_ERROR.format(error='missing section in {0}'.format(configfiles)))
            self.logger.error(RED_ERROR.format(error='check the name of the config file'))
            self.logger.info("Try `optimizer help` and `optimizer fetch`")
            return 
        return self.optimizer
    
    def clean_up(self, error):
        """
        To be called by the try-except if an exception is caught
        """
        if type(error) is KeyboardInterrupt:
            log_error(error, self.logger, 'Oh, I am slain!')
            if self.optimizer is not None:                
                self.optimizer.clean_up(error)
        else:
            log_error(error, self.logger, self.error_message)
        return
        
#
