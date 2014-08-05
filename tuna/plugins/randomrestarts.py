
# python standard library
from collections import OrderedDict

# third-party
import numpy

# this package
from tuna.infrastructure import singletons
from tuna import GLOBAL_NAME
from base_plugin import BasePlugin
from tuna.parts.storage.storageadapter import StorageAdapter
from tuna.parts.storage.nullstorage import NullStorage

from tuna.optimizers.randomrestarts import RandomRestarter

from tuna.parts.stopcondition import StopConditionGeneratorBuilder

from tuna.tweaks.convolutions import GaussianConvolutionBuilder
from tuna.tweaks.convolutions import GaussianConvolutionConstants
from tuna.tweaks.convolutions import XYConvolutionBuilder
from tuna.tweaks.convolutions import XYConvolutionConstants

from tuna.parts.stopcondition import StopConditionConstants
from tuna.parts.xysolution import XYTweak, XYSolution
from tuna.qualities.qualitycomposite import QualityCompositeBuilder
from tuna.components.composite import SimpleCompositeBuilder



in_pweave = __name__ == '__builtin__'


ANNEALINGSECTION = 'RandomRestarts'
CONFIGURATION = '''[{section}]
# the section-name has to match an option in the TUNA section
# the plugin has to be the actual class name
plugin = RandomRestarts

# to assess how things went, set store_output to a filename and it will
# save the solutions found to it (comma-separated)
# store_output = annealing_solutions_{{{{timestamp}}}}.csv

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

# random-restart parameters
# this sets the boundaries for local-search-times
# so they should be times (e.g. 2 minutes)
{max_time} = <maximum local search time>
{min_time} = <minimum local search time>

# input parameters
# these are for the random number generator
# the default convolution assumes the same bounds for all entries in the vector
# change to XYConvolution for the asymmetric 2-space case
#tweak_type = <type of convolution>
tweak_type = GaussianConvolution

# the lower and upper bounds have to match the inputs for the thing being tested
{num_type} = <input number type (int or float)>
{low} = <allowed lower bound for inputs>
{upper} = <allowed upper bound for inputs>

# location is where the random changes will be centered (0 means equal chance positive or negative)
# scale is how spread out the changes will be (bigger numbers, more randomness)
#{location} = <center of random distribution (default={loc_default})>
#{scale} = <spread of random distribution (default={scale_default})>

# stopping conditions
{end} = <time to stop trying to improve (any reasonable time-stamp)>
{time_limit} = <amount of time to try (if end_time not given)>

# an optional ideal value (float) can be given to stop the search
#{ideal} = <stop if this value is reached>
#{delta} = <difference from ideal to tolerate (default={delta_default})>
'''.format(section=ANNEALINGSECTION,
           num_type=GaussianConvolutionConstants.number_type,
           location=GaussianConvolutionConstants.location,
           loc_default=GaussianConvolutionConstants.location_default,
           low=GaussianConvolutionConstants.lower_bound,
           upper=GaussianConvolutionConstants.upper_bound,
           scale=GaussianConvolutionConstants.scale,
           scale_default=GaussianConvolutionConstants.scale_default,
           max_time=StopConditionConstants.maximum_time,
           min_time=StopConditionConstants.minimum_time,
            end=StopConditionConstants.end_time,
            time_limit=StopConditionConstants.time_limit,
            ideal=StopConditionConstants.ideal,
            delta=StopConditionConstants.delta,
            delta_default=StopConditionConstants.default_delta)


output_documentation = __name__ == '__builtin__'


class RandomRestarts(BasePlugin):
    """
    A hill-climbing with random-restarts plugin
    """
    def __init__(self, *args, **kwargs):
        """
        RandomRestarts plugin Constructor

        """
        super(RandomRestarts, self).__init__(*args, **kwargs)
        self._tweak = None
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
    def tweak(self):
        """
        An object to 'tweak' the candidate solution
        """
        if self._tweak is None:
            tweak_type = self.configuration.get(section=self.section_header,
                                                option='tweak_type',
                                                optional=True,
                                                default='gaussianconvolution')
            if tweak_type.lower().startswith('xy'):
                tweak = XYConvolutionBuilder(configuration=self.configuration,
                                         section=self.section_header).product
            else:
                tweak = GaussianConvolutionBuilder(configuration=self.configuration,
                                               section=self.section_header).product
            
            self._tweak = XYTweak(tweak)
        return self._tweak


    @property
    def sections(self):
        """
        An ordered dictionary for the HelpPage
        """
        if self._sections is None:
            bold = '{bold}'
            reset = '{reset}'
            name = 'RandomRestarts'
            bold_name = bold + name + reset

            self._sections = OrderedDict()
            self._sections['Name'] = '{blue}' + name + reset + ' -- hill-climbing with random restarts optimizer'
            self._sections['Description'] = bold_name + ' optimizes using hill-climbing with random restarts.'
            self._sections["Configuration"] = CONFIGURATION
            self._sections['Files'] = __file__
        return self._sections
    
    @property
    def product(self):
        """
        This is the RandomRestarter product

        To allow repeated running the RandomRestarter is created anew every time

        :precondition: self.configuration is a configuration map
        """
        kwargs = dict(self.configuration.items(section=self.section_header,
                                                   optional=False))
        self.logger.debug("Building the RandomRestarter with: {0}".format(kwargs))


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

        candidate = self.configuration.get_list(section=self.section_header,
                                                option='candidate',
                                                optional=True)

        # this needs to be made smarter
        if candidate is not None:
            candidate = XYSolution(numpy.array([float(item) for item in candidate]))

        stop_conditions = StopConditionGeneratorBuilder(configuration=self.configuration,
                                                        section=self.section_header).product

        self._product = RandomRestarter(local_stops=stop_conditions,
                                          tweak=self.tweak,
                                          quality=quality,
                                          candidate=candidate,
                                          solution_storage=self.storage,
                                          global_stop=stop_conditions.global_stop_condition,
                                          observers=observers)
        return self._product
        
    def fetch_config(self):
        """
        Prints example configuration to stdout
        """
        print CONFIGURATION
# end class RandomRestarts
