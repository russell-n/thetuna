
# python standard library
from collections import OrderedDict

# tuna
from component import BaseComponent
from tuna import ConfigurationError
from tuna.plugins.base_plugin import BasePlugin
from tuna.parts.dummy.dummy import DummyClass


CONFIGURATION = """
[Dummy]
# this follows the pattern for plugins --
# the header has to match what's in the Optimizers `components` list
# the component option has to be DummyComponent
component = Dummy

# Everything else is arbitrary
"""

DESCRIPTION = """
The DummyComponent is a placeholder for components that can't be run. It will reflect (to stdout) the calls made to it.
"""


class DummyComponent(BaseComponent):
    """
    A fake component
    """
    def __init__(self, *args, **kwargs):
        """
        DummyComponent Constructor

        """
        super(DummyComponent, self).__init__()
        self.dummy = DummyClass(*args, **kwargs)
        return

    def __call__(self, *args, **kwargs):
        """
        Sends arguments to the dummy
        """
        self.dummy(*args, **kwargs)
        return 

    def check_rep(self):
        """
        Checks the dummy
        """
        self.dummy.check_rep()
        return

    def close(self):
        """
        closes the dummy
        """
        self.dummy.close()
        return

    def reset(self):
        """
        resets the dummy
        """
        self.dummy.reset()
        return
# end DummyComponent


class Dummy(BasePlugin):
    """
    Builds Dummy objects from configuration-maps
    """
    def __init__(self, *args, **kwargs):
        """
        Dummy constructor

        """
        super(Dummy, self).__init__(*args, **kwargs)
        return

    @property
    def product(self):
        """
        A built DummyComponent object
        """
        if self._product is None:
            kwargs = dict(self.configuration.items(section=self.section_header,
                                                   optional=False))
            self._product = DummyComponent(**kwargs)
        return self._product

    @property
    def sections(self):
        """
        An ordered dictionary for the HelpPage
        """
        if self._sections is None:
            bold = '{bold}'
            reset = '{reset}'
            name = 'Dummy'
            bold_name = bold + name + reset

            self._sections = OrderedDict()
            self._sections['Name'] = '{blue}' + name + reset + ' -- A component for missing parts'
            self._sections['Description'] = bold_name + DESCRIPTION
            self._sections["Configuration"] = CONFIGURATION
            self._sections['Files'] = __file__
        return self._sections

    def fetch_config(self):
        """
        prints sample configuration to the scree
        """
        print CONFIGURATION
        return

