
"""`run` sub-command

Usage: tuna run -h
       tuna run [<configuration>...]

Positional Arguments:

    <configuration>   0 or more configuration-file names [default: optimizer.ini]

Options;

    -h, --help  This help message.

"""


# python standard library
import datetime

# the TUNA
from tuna import RED, BOLD, RESET
from tuna.infrastructure.arguments.arguments import BaseArguments
from tuna.infrastructure.arguments.basestrategy import BaseStrategy
from tuna.infrastructure.crash_handler import try_except


class RunArgumentsConstants(object):
    """
    Constants for the Run Arguments
    """
    __slots__ = ()
    configfiles = '<configuration>'
    
    # defaults
    default_configfiles = ['tuna.ini']
# RunArgumentsConstants    


class Run(BaseArguments):
    """
    run a configuration
    """
    def __init__(self, *args, **kwargs):
        super(Run, self).__init__(*args, **kwargs)
        self._configfiles = None
        self.sub_usage = __doc__
        self._function = None
        return

    @property
    def function(self):
        """
        sub-command function 
        """
        if self._function is None:
            self._function = RunStrategy().function
        return self._function

    @property
    def configfiles(self):
        """
        List of config-file names
        """
        if self._configfiles is None:
            self._configfiles = self.sub_arguments[RunArgumentsConstants.configfiles]
            if not self._configfiles:
                self._configfiles = RunArgumentsConstants.default_configfiles
        return self._configfiles

    def reset(self):
        """
        Resets the attributes to None
        """
        super(Run, self).reset()
        self._configfiles = None
        return
# end RunArguments        


INFO_STRING = '{b}**** {{0}} ****{r}'.format(b=BOLD, r=RESET)


class RunStrategy(BaseStrategy):
    """
    The strategy for the `run` sub-command
    """
    @try_except
    def function(self, args):
        """
        Builds and runs the test
        """
        self.logger.info(INFO_STRING.format("Starting The TUNA"))
        start = datetime.datetime.now()
        
        tuna = self.build_tuna(args.configfiles)
        
        if tuna is None:
            return
        
        # the main run (the others are for debugging)
        tuna()

        tuna.close()
        end = datetime.datetime.now()
        self.logger.info(INFO_STRING.format("Total Elapsed Time: {0}".format(end-start)))
        return
