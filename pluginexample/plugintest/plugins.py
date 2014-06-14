from tuna import BasePlugin
from tuna.parts.dummy.dummy import DummyClass

from collections import OrderedDict

HELP = """
[PLUGINTEST]
plugin = PluginTest
name = something
blah = blahblahblah
"""

SECTIONS = OrderedDict()
SECTIONS['Name'] = "{bold}PLuginTest{reset} --  a dummy plugin"
SECTIONS['Blah'] = "blah, blah, blah,..."

class PluginTest(BasePlugin):
    """
    A plugin to test
    """
    def __init__(self, *args, **kwargs):
        super(PluginTest, self).__init__(*args, **kwargs)
        return    

    def fetch_config(self):
        print HELP

    @property
    def sections(self):
        return SECTIONS

    @property
    def product(self):
        kwargs = dict(self.configuration.items('PLUGINTEST', optional=True, default={}))
        return DummyClass(**kwargs)
        
