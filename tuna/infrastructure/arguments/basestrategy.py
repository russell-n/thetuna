
# python standard library
from ConfigParser import NoSectionError
import datetime

# this package
from tuna import BaseClass

from tuna.infrastructure.crash_handler import try_except, log_error
from tuna import RED, BOLD, RESET
from tuna.infrastructure.quartermaster import QuarterMaster


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
        self.tuna = None
        return

    quartermaster = QuarterMaster()

    def build_tuna(self, configfiles):
        """
        Tries to build the tuna plugin
        (has a side-effect of setting self.tuna so that crash-handling can get to it)

        :return: optimizer or None
        :postcondition: self.tuna set to tuna (or None on failure)

        :param: `configfiles`: a list of configuration files for the optimizer
        """
        plugin = self.quartermaster.get_plugin('Tuna')
        
        # The tuna needs the config-filenames
        try:
            self.tuna = plugin(configfiles=configfiles).product
        except NoSectionError as error:
            self.logger.error(error)
            self.logger.error(RED_ERROR.format(error='missing section in {0}'.format(configfiles)))
            self.logger.error(RED_ERROR.format(error='check the name of the config file'))
            self.logger.info("Try `tuna help` and `tuna fetch`")
            return 
        return self.tuna
    
    def clean_up(self, error):
        """
        To be called by the try-except if an exception is caught
        """
        if type(error) is KeyboardInterrupt:
            log_error(error, self.logger, 'Oh, I am slain!')
            if self.tuna is not None:                
                self.tuna.clean_up(error)
        else:
            log_error(error, self.logger, self.error_message)
        return
        
#
