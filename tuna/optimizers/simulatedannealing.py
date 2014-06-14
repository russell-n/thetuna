
# python standard library
import random
import math

# this package
from tuna.components.component import BaseComponent
from tuna import BaseClass, ConfigurationError


class SimulatedAnnealer(BaseComponent):
    """
    a Simulated Annealer optimizer
    """
    def __init__(self, temperatures, tweak, quality, candidate, stop_condition,
                 solution_storage=None):
        """
        SimulatedAnnealer Constructor

        :param:

         - `temperatures`: a generator of temperatures
         - `tweak`: callable that tweaks the best solution so far
         - `quality`: Quality checker for candidates
         - `candidate`: initial candidate solution
         - `stop_condition`: a condition to decide to prematurely stop
         - `solution_storage`: a callable to send solutions to
        """
        self.temperatures = temperatures
        self.tweak = tweak
        self.quality = quality
        self.solution = candidate
        self.stop_condition = stop_condition
        self._solutions = solution_storage
        return

    @property
    def solutions(self):
        """
        object with `append` method to save solutions
        """
        if self._solutions is None:
            self._solutions = []
        return self._solutions

    def check_rep(self):
        """
        should validate the parameters
        """
        return

    def close(self):
        """
        closes the quality and solutions' storage
        """
        self.quality.close()
        self.solutions.close()
        return

    def __call__(self):
        """
        Runs the optimization

        :return: last non-None output given
        """
        solution = self.solution
        # prime the data with the first candidate
        self.quality(solution)
        self.solutions.append(solution)
        
        for temperature in self.temperatures:
            candidate = self.tweak(solution)
            
            quality_difference = self.quality(candidate) - self.quality(solution)
            if (quality_difference > 0 or
                random.random() < math.exp(quality_difference/float(temperature))):
                solution = candidate
            if self.quality(solution) > self.quality(self.solution):
                self.solutions.append(solution)
                self.solution = solution
            if self.stop_condition(self.solution):
                break
        return self.solution
# SimulatedAnnealer    


class TemperatureGenerator(object):
    """
    A class to generate temperature drops for the annealing
    """
    def __init__(self, start, stop=0, schedule=lambda x: x-1):
        """
        TemperatureGenerator constructor

        :param:

         - `start`: starting temperature
         - `stop`: stopping temperature
        """
        self.start = start
        self.stop = stop
        self.schedule = schedule
        return

    def __iter__(self):
        """
        Generates decreasing temperatures

        :yield: next temperature in the schedule
        """
        temperature = self.start
        while temperature >= self.stop:
            yield temperature
            temperature = self.schedule(temperature)
        return
# end class TemperatureGenerator    


class TimeTemperatureGenerator(object):
    """
    A Generator of temperatures using repetitions
    """
    def __init__(self, start, stop, alpha):
        """
        TimeTemperatureGenerator constructor

        :param:

         - `start`: starting temperature (T_0)
         - `stop: stopping temperature
         - `alpha`: constant value used by the schedule
        """
        self.start = start
        self.stop = stop
        self.alpha = alpha
        self.time = -1
        return

    def schedule(self):
        """
        Method that returns the next temperature

        increments self.time and returns next time in geometric progression
        """
        self.time += 1        
        return self.start * self.alpha**self.time

    def __iter__(self):
        """
        Iterator to yield temperatures
        """
        temperature = self.schedule()
        while temperature > self.stop:
            yield temperature
            temperature = self.schedule()
        return

    def close(self):
        """
        Resets the time to -1 so the iterator can be re-used
        """
        self.time = -1
        return
# end TimeTemperatureGenerator    


# this is for clients so the strings are consistent
class TimeTemperatureGeneratorConstants(object):
    __slots__ = ()
    # the config file needs to be wordier
    # so the option-names are longer
    # options
    start = 'start_temperature'
    stop = 'stop_temperature'
    alpha = 'alpha_temperature'


class TimeTemperatureGeneratorBuilder(BaseClass):
    """
    Builds the TimeTemperatureGenerator from a dictionary
    """
    def __init__(self, configuration, section):
        """
        TimeTemperatureGeneratorBuilder constructor
        
        :param:

         - `configuration`: a configuration map
         - `section`: name of section with options
        """
        super(TimeTemperatureGeneratorBuilder, self).__init__()
        self.configuration = configuration
        self.section = section
        self._product = None
        return

    @property
    def product(self):
        """
        A built time-temperature generator
        """
        if self._product is None:
            constants = TimeTemperatureGeneratorConstants
            config = self.configuration
            try:
                self._product = TimeTemperatureGenerator(start=config.get_float(section=self.section,
                                                                                option=constants.start),
                                                         stop=config.get_float(section=self.section,
                                                                               option=constants.stop),
                                                         alpha=config.get_float(section=self.section,
                                                                                option=constants.alpha))
            except KeyError as error:
                self.logger.error("Missing Option: {0}".format(error))
                raise ConfigurationError("Unable to build the TimeTemperatureGenerator with '{0}'".format(self.configuration))
            except ValueError as error:
                self.logger.error(error)
                self.log_error("Temperature values must be castable to floats")
                raise ConfigurationError("Unable to build the TimeTemperatureGenerator with '{0}'".format(self.configuration))
        return self._product
