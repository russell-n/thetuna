
# python standard library
from collections import OrderedDict

# third-party
# this is for testing only
import numpy

# this package
from tuna.infrastructure import singletons
from tuna import GLOBAL_NAME
from base_plugin import BasePlugin
from tuna.parts.dummy.dummy import DummyClass
from tuna.parts.storage.storageadapter import StorageAdapter
from tuna.optimizers.simulatedannealing import SimulatedAnnealer
from tuna.optimizers.simulatedannealing import TimeTemperatureGeneratorConstants
from tuna.parts.stopcondition import StopConditionBuilder
from tuna.optimizers.simulatedannealing import TimeTemperatureGeneratorBuilder
from tuna.tweaks.convolutions import GaussianConvolutionBuilder
from tuna.tweaks.convolutions import GaussianConvolutionConstants
from tuna.parts.stopcondition import StopConditionConstants
from tuna.parts.xysolution import XYTweak, XYSolution
from tuna.qualities.dataquality import DataQualityXYBuilder


in_pweave = __name__ == '__builtin__'


ANNEALINGSECTION = 'Annealing'
CONFIGURATION = '''[{section}]
# since the plugin is specified, the section-name 
# just has to match an option in the TUNA section
plugin = SimulatedAnnealing

# annealing parameters
{start} = <starting temperature (should be high)>
{stop} = <stopping temperature (should be around 0)>
{alpha} = <change constant (0 < alpha < 1)>

# input parameters
{num_type} = <input number type (int or float)>
{low} = <allowed lower bound for inputs>
{upper} = <allowed upper bound for inputs>
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
        return

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
                                                   optional=False))
            self.logger.debug("Building the Simulated Annealer with: {0}".format(kwargs))

            temperatures = TimeTemperatureGeneratorBuilder(configuration=self.configuration,
                                                           section=self.section_header).product
            tweak = GaussianConvolutionBuilder(configuration=self.configuration,
                                               section=self.section_header).product
            xytweak = XYTweak(tweak)
            quality = DataQualityXY()

            candidate = XYSolution(numpy.array([3]))

            stop_condition = StopConditionBuilder(configuration=self.configuration,
                                                  section=self.section_header).product            
            storage = singletons.get_filestorage(name=GLOBAL_NAME)
            opened_file = storage.open('annealing_solutions.csv')
            adapter = StorageAdapter(storage=opened_file)
            self._product = SimulatedAnnealer(temperatures=temperatures,
                                              tweak=xytweak,
                                              quality=quality,
                                              candidate=candidate,
                                              solution_storage=adapter,
                                              stop_condition=stop_condition)
        return self._product
        
    def fetch_config(self):
        """
        Prints example configuration to stdout
        """
        print CONFIGURATION
# end class SimulatedAnnealing
