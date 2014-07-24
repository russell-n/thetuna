
# python standard library
from collections import OrderedDict

# third-party
# this is for testing only
import numpy

# this package
from tuna.infrastructure import singletons
from tuna import GLOBAL_NAME
from base_plugin import BasePlugin
from tuna.parts.storage.storageadapter import StorageAdapter
from tuna.parts.storage.nullstorage import NullStorage

from tuna.optimizers.simulatedannealing import SimulatedAnnealer
from tuna.optimizers.simulatedannealing import TimeTemperatureGeneratorConstants
from tuna.parts.stopcondition import StopConditionBuilder
from tuna.optimizers.simulatedannealing import TimeTemperatureGeneratorBuilder
from tuna.tweaks.convolutions import GaussianConvolutionBuilder
from tuna.tweaks.convolutions import GaussianConvolutionConstants
from tuna.tweaks.convolutions import XYConvolutionBuilder
from tuna.tweaks.convolutions import XYConvolutionConstants

from tuna.parts.stopcondition import StopConditionConstants
from tuna.parts.xysolution import XYTweak, XYSolution
from tuna.qualities.qualitycomposite import QualityCompositeBuilder
from tuna.components.composite import SimpleCompositeBuilder



in_pweave = __name__ == '__builtin__'


ANNEALINGSECTION = 'Annealing'
CONFIGURATION = '''[{section}]
# since the plugin is specified, the section-name 
# just has to match an option in the TUNA section
plugin = SimulatedAnnealing

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

# annealing parameters
{start} = <starting temperature (should be high)>
{stop} = <stopping temperature (should be around 0)>
# alpha closer to 1 means slower descent
{alpha} = <change constant (0 < alpha < 1)>

# input parameters
# these are for the random number generator
# the default convolution assumes the same bounds for all entries in the vector
# change to XYConvolution for the asymmettric 2-space case
#tweak_type = <type of convolution>

# the lower and upper bounds have to match the inputs for the thing being tested
{num_type} = <input number type (int or float)>
{low} = <allowed lower bound for inputs>
{upper} = <allowed upper bound for inputs>

# location is where the random changes will be centered (0 means equal chance positive or negative)
# scale is how spread out the changes will be (bigger numbers, more randomness)
{location} = <center of random distribution (default={loc_default})>
{scale} = <spread of random distribution (default={scale_default})>

# stopping conditions
{end} = <time to stop trying to improve (any reasonable time-stamp)>
{time_limit} = <amount of time to try (if end_time not given)>
{ideal} = <stop if this value is reached>
{delta} = <difference from ideal to tolerate (default={delta_default})>
'''.format(section=ANNEALINGSECTION,
           start=TimeTemperatureGeneratorConstants.start,
           stop=TimeTemperatureGeneratorConstants.stop,
           alpha=TimeTemperatureGeneratorConstants.alpha,
           num_type=GaussianConvolutionConstants.number_type,
           location=GaussianConvolutionConstants.location,
           loc_default=GaussianConvolutionConstants.location_default,
           low=GaussianConvolutionConstants.lower_bound,
           upper=GaussianConvolutionConstants.upper_bound,
           scale=GaussianConvolutionConstants.scale,
           scale_default=GaussianConvolutionConstants.scale_default,

            end=StopConditionConstants.end_time,
            time_limit=StopConditionConstants.time_limit,
            ideal=StopConditionConstants.ideal,
            delta=StopConditionConstants.delta,
            delta_default=StopConditionConstants.default_delta)


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
            name = 'SimulatedAnnealing'
            bold_name = bold + name + reset

            self._sections = OrderedDict()
            self._sections['Name'] = '{blue}' + name + reset + ' -- simulated annealing optimizer'
            self._sections['Description'] = bold_name + ' Runs a simulated annealing optimizer.'
            self._sections["Configuration"] = CONFIGURATION
            self._sections['Files'] = __file__
        return self._sections
    
    @property
    def product(self):
        """
        This is the SimulatedAnnealing product

        To allow repeated running the SimulatedAnnealer is created anew every time

        :precondition: self.configuration is a configuration map
        """
        kwargs = dict(self.configuration.items(section=self.section_header,
                                                   optional=False))
        self.logger.debug("Building the Simulated Annealer with: {0}".format(kwargs))

        temperatures = TimeTemperatureGeneratorBuilder(configuration=self.configuration,
                                                       section=self.section_header).product

        quality = QualityCompositeBuilder(configuration=self.configuration,
                                          section_header=self.section_header).product

        observers = self.configuration.get(self.section_header, 'observers', optional=True)
        if observers is not None:
            observers = SimpleCompositeBuilder(configuration=self.configuration,
                                               section_header=self.section_header,
                                               option='observers').product
            # set them up so they always act, even though target.output was set
            for observer in observers:
                observer.always = True
        candidate = self.configuration.get_list(section=self.section_header,
                                                option='candidate',
                                                optional=True)

        # this needs to be made smarter
        if candidate is not None:
            candidate = XYSolution(numpy.array([float(item) for item in candidate]))

        stop_condition = StopConditionBuilder(configuration=self.configuration,
                                                  section=self.section_header).product

        self._product = SimulatedAnnealer(temperatures=temperatures,
                                          tweak=self.tweak,
                                          quality=quality,
                                          candidate=candidate,
                                          solution_storage=self.storage,
                                          stop_condition=stop_condition,
                                          observers=observers)
        return self._product
        
    def fetch_config(self):
        """
        Prints example configuration to stdout
        """
        print CONFIGURATION
# end class SimulatedAnnealing
