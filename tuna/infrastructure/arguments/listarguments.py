
"""`list` subcommand

usage: tuna list -h
       tuna list [--components] [<module> ...]

Positional Arguments:
  <module> ...  Space-separated list of importable module with plugins

optional arguments:

  -h, --help                 Show this help message and exit
  -c, --components           List `components` instead of `plugins`

"""


# the tuna
from tuna.infrastructure.crash_handler import try_except
from tuna.infrastructure.arguments.arguments import BaseArguments
from tuna.infrastructure.arguments.basestrategy import BaseStrategy
from tuna.components.component import BaseComponent


class ListArgumentsConstants(object):
    """
    Constants for the list sub-command arguments
    """
    __slots__ = ()
    # arguments
    modules = "<module>"
    components = '--components'


class List(BaseArguments):
    """
    list known plugins
    """
    def __init__(self, *args, **kwargs):
        super(List, self).__init__(*args, **kwargs)
        self._modules = None
        self.sub_usage = __doc__
        self._function = None
        self._components = None
        return

    @property
    def function(self):
        """
        The `list` sub-command
        """
        if self._function is None:
            self._function = ListStrategy().function
        return self._function

    @property
    def modules(self):
        """
        List of external modules holding plugins
        """
        if self._modules is None:
            self._modules = self.sub_arguments[ListArgumentsConstants.modules]
        return self._modules

    @property
    def components(self):
        """
        Boolean to switch to components instead of plugins
        """
        if self._components is None:
            self._components = self.sub_arguments[ListArgumentsConstants.components]
        return self._components

    def reset(self):
        """
        Resets the attributes to None
        """
        super(List, self).reset()
        self._modules = None
        return
# end List


class ListStrategy(BaseStrategy):
    """
    The strategy for the 'list' sub-command
    """    
    @try_except
    def function(self, args):
        """
        The function to run for this strategy (instead of the ArgParse sub-command function).
        Uses the QuarterMaster to list the plugins or components

        :param:

         - `args`: object with `modules` and `components` attribute
        """
        if args.components:
            self.quartermaster.name = 'components'
            self.quartermaster.exclusions.append('tuna.components.composite')
        self.quartermaster.external_modules = args.modules
        self.quartermaster.list_plugins()
        return
