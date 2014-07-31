
# python standard library
from collections import OrderedDict

# third-party
import numpy

# this package
from tuna.infrastructure import singletons
from tuna.parts.storage.storageadapter import StorageAdapter
from tuna.parts.storage.nullstorage import NullStorage

from tuna import GLOBAL_NAME
from base_plugin import BasePlugin

from tuna.optimizers.exhaustivesearch import ExhaustiveSearchBuilder
from tuna.optimizers.exhaustivesearch import ExhaustiveSearchConstants

from tuna.qualities.qualitycomposite import QualityCompositeBuilder
from tuna.components.composite import SimpleCompositeBuilder


in_pweave = __name__ == '__builtin__'


SECTION = 'GridSearch'
CONFIGURATION = '''[{section}]
# The section name has to match an option in the TUNA section
plugin = GridSearch

# the components are the things that are given the input values
# to get the output values (e.g. a component that measures iperf)
# to see the known components use `tuna list -c`
# the names in the list are meant to match a section header in the
# configuration file so can be arbitrary
# each section needs a 'component=<component>' line 
components = <comma-separated list of sections with component options>

# observers will be called once after the annealing is done
# they will be called passing in the best solution found
# like the components, each section needs a 'component = <component>' line
# observers = <comma-separated list of sections with observer-component options>

# search parameters
{minima} = <comma-separated list representing starting coordinates (e.g. 0,0)>
{maxima} = <comma-separated list representing ending coordinate (e.g. 59,59)>
{increments} = <comma-separated list representing how much to increment the coordinates>
{dtype} = <data-type for grid-coordinates (e.g. dtype=int)>

# e.g. if you want to sweep a 1500 x 3000 grid 50 positions at a time:
# {minima} = 0,0
# {maxima} = 1500,3000
# {increments} = 50

# to save the data give a file name to 'store_output'
# if commented out it won't save anything
# store_output = grid_search.csv
'''.format(section=SECTION,
           minima=ExhaustiveSearchConstants.minima_option,
           maxima=ExhaustiveSearchConstants.maxima_option,
           increments=ExhaustiveSearchConstants.increments_option,
           dtype=ExhaustiveSearchConstants.datatype_option)


output_documentation = __name__ == '__builtin__'


class GridSearch(BasePlugin):
    """
    A grid-searching plugin
    """
    def __init__(self, *args, **kwargs):
        """
        GridSearch plugin Constructor
        """
        super(GridSearch, self).__init__(*args, **kwargs)
        self._storage = None
        return

    @property
    def storage(self):
        """
        A storage for solutions
        """
        if self._storage is None:
            filename =  self.configuration.get(section=self.section_header,
                                              option='store_output',
                                              optional=True)
            if filename is not None:
                storage = singletons.get_filestorage(name=GLOBAL_NAME)

                self._storage = StorageAdapter(storage=storage, filename=filename)
            else:
                self._storage = NullStorage()
        return self._storage                

    @property
    def sections(self):
        """
        An ordered dictionary for the HelpPage
        """
        if self._sections is None:
            bold = '{bold}'
            reset = '{reset}'
            name = 'GridSearch'
            bold_name = bold + name + reset

            self._sections = OrderedDict()
            self._sections['Name'] = '{blue}' + name + reset + ' -- GridSearch optimizer'
            self._sections['Description'] = bold_name + ' Runs an exhaustive grid-searching optimizer.'
            self._sections["Configuration"] = CONFIGURATION
            self._sections['Files'] = __file__
        return self._sections
    
    @property
    def product(self):
        """
        This is the ExhaustiveSearch product

        To allow repeated running the ExhaustiveSearch is created anew every time

        :precondition: self.configuration is a configuration map
        """
        kwargs = dict(self.configuration.items(section=self.section_header,
                                                   optional=False))
        self.logger.debug("Building the GridSearch with: {0}".format(kwargs))

        quality = QualityCompositeBuilder(configuration=self.configuration,
                                          section_header=self.section_header).product

        observers = self.configuration.get(self.section_header, 'observers', optional=True)
        if observers is not None:
            observers = SimpleCompositeBuilder(configuration=self.configuration,
                                               section_header=self.section_header,
                                               option='observers').product
            # make it so they do something with the last solution even though target.output is set
            for observer in observers:
                observer.always = True



        self._product = ExhaustiveSearchBuilder(configuration=self.configuration,
                                                section_header=self.section_header,
                                                quality=quality,
                                                solution_storage=self.storage,
                                                observers=observers).product
        return self._product
        
    def fetch_config(self):
        """
        Prints example configuration to stdout
        """
        print CONFIGURATION
# end class SimulatedAnnealing
