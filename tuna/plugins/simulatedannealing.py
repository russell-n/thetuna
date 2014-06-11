
# python standard library
from collections import OrderedDict

# this package
from base_plugin import BasePlugin
from tuna.parts.dummy.dummy import DummyClass
from tuna.optimizers.simulatedannealing import SimulatedAnnealer


in_pweave = __name__ == '__builtin__'


ANNEALINGSECTION = 'Annealing'
CONFIGURATION = '''[{0}]
# since the plugin is specified, the section-name 
# just has to match an option in the TUNA section
plugin = SimulatedAnnealing

arbitrary_option = arbitrary arguments
'''.format(ANNEALINGSECTION)



output_documentation = __name__ == '__builtin__'


class SimulatedAnnealing(BasePlugin):
    """
    A simulated annealing plugin
    """
    def __init__(self, *args, **kwargs):
        """
        SimulatedAnnealing plugin Constructor

        """
        super(SimulatedAnnealing, self).__init__(*args, **kwargs)
        return

    @property
    def sections(self):
        """
        An ordered dictionary for the HelpPage
        """
        if self._sections is None:
            bold = '{bold}'
            reset = '{reset}'
            
            bold_name = bold + name + reset

            self._sections = OrderedDict()
            self._sections['Name'] = '{blue}' + name + reset + ' -- simulated annealing optimizer'
            self._sections['Description'] = bold_name + ' Runs a simulated annealing optimizer.'.format(ANNEALINGSECTION)
            self._sections["Configuration"] = CONFIGURATION
            self._sections['Files'] = __file__
        return self._sections
    
    @property
    def product(self):
        """
        This is the SimulatedAnnealing product

        :precondition: self.configuration is a configuration map
        """
        if self._product is None:
            kwargs = dict(self.configuration.items(section=self.section_header,
                                                   optional=True,
                                                   default={}))
            #DummyClass(**kwargs)
            temperatures = reversed(xrange(10))
            tweak = lambda x: x + 1
            #quality = lambda x: x + 2
            class Fake(object):
                def __call__(self, value):
                    return value + 2

                def close(self):
                    pass

            quality = Fake()
            candidate = 3
            stop_condition = DummyClass()
            storage = DummyClass()
            self._product = SimulatedAnnealer(temperatures=temperatures,
                                              tweak=tweak,
                                              quality=quality,
                                              candidate=candidate,
                                              solution_storage=storage,
                                              stop_condition=stop_condition)
        return self._product
        
    def fetch_config(self):
        """
        Prints example configuration to stdout
        """
        print CONFIGURATION
# end class SimulatedAnnealing
