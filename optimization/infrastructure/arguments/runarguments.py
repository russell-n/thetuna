
"""`run` sub-command

Usage: optimizer run -h
       optimizer run [<configuration>...]

Positional Arguments:

    <configuration>   0 or more configuration-file names [default: optimizer.ini]

Options;

    -h, --help  This help message.

"""


# python standard library
import datetime

# the OPTIMIZER
from optimization import RED, BOLD, RESET
from optimization.infrastructure.arguments.arguments import BaseArguments
from optimization.infrastructure.arguments.basestrategy import BaseStrategy
from optimization.infrastructure.crash_handler import try_except


class RunArgumentsConstants(object):
    """
    Constants for the Run Arguments
    """
    __slots__ = ()
    configfiles = '<configuration>'
    
    # defaults
    default_configfiles = ['optimizer.ini']
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
        self.logger.info(INFO_STRING.format("Starting The OPTIMIZER"))
        start = datetime.datetime.now()
        
        optimizer = self.build_optimizer(args.configfiles)
        
        if optimizer is None:
            return
        
        if args.trace:
            import trace
        
            tracer = trace.Trace(trace=True,
                                 ignoremods= ['__init__', 'handlers',
                                              'threading', 'genericpath',
                                              'posixpath'],
                                              timing=True)
            tracer.runfunc(optimizer)

        elif args.callgraph:
            from pycallgraph import PyCallGraph
            from pycallgraph import GlobbingFilter
            from pycallgraph import Config
            from pycallgraph.output import GraphvizOutput
            
            config = Config(max_depth=10)
            graphviz = GraphvizOutput()
            graphviz.output_file = 'optimizer_callgraph.png'
            with PyCallGraph(output=graphviz, config=config):
                optimizer()

        else:
            # the main run (the others are for debugging)
            optimizer()

        optimizer.close()
        end = datetime.datetime.now()
        self.logger.info(INFO_STRING.format("Total Elapsed Time: {0}".format(end-start)))
        return
