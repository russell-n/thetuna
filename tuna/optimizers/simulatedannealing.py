
# python standard library
import random
import math
import datetime

# this package
from tuna.components.component import BaseComponent
from tuna import BaseClass, ConfigurationError
from tuna import LOG_TIMESTAMP


ANNEALING_SOLUTIONS = "annealing_solutions.csv"


class SimulatedAnnealer(BaseComponent):
    """
    a Simulated Annealer optimizer
    """
    def __init__(self, temperatures, tweak, quality, candidate, stop_condition,
                 solution_storage, observers=None):
        """
        SimulatedAnnealer Constructor

        :param:

         - `temperatures`: a generator of temperatures
         - `tweak`: callable that tweaks the best solution so far
         - `quality`: Quality checker for candidates
         - `candidate`: initial candidate solution
         - `stop_condition`: a condition to decide to prematurely stop
         - `solution_storage`: an writeable object to send values to
         - `observers`: a composite that takes the best solution as its argument
        """
        super(SimulatedAnnealer, self).__init__()
        self.temperatures = temperatures
        self.tweak = tweak
        self.quality = quality
        self.candidate = candidate
        self._solution = candidate
        self.stop_condition = stop_condition
        self.solutions = solution_storage
        self.observers = observers
        self.tabu = []
        return

    @property
    def solution(self):
        """
        Current candidate solution
        """
        if self._solution is None:
            if self.candidate is not None:
                self._solution = self.candidate
            else:
                self._solution = self.tweak()
        return self._solution

    @solution.setter
    def solution(self, candidate):
        """
        Sets the solution
        """
        self._solution = candidate
        return

    def check_rep(self):
        """
        should validate the parameters
        """
        return

    def close(self):
        """
        closes the quality and solutions' storage and resets the solution to None
        """
        self.quality.close()
        self.solutions.close()        
        self._solution = None
        return

    def reset(self):
        self.logger.debug("Resetting the annealing parts")
        self.tabu = []
        self.quality.reset()
        self.temperatures.reset()
        self._solution = None
        self.solutions.reset()
        self.stop_condition.reset()
        return

    def __call__(self):
        """
        Runs the optimization

        :return: last best solution found
        """
        # this is an attempt to allow this to run repeatedly
        # the solutions can't be a list anymore
        self.reset()
        # prime the data with the first candidate
        solution = self.solution
        self.quality(solution)
        
        # avoid repeating the same test-spot
        self.tabu.append(str(solution.inputs))
        
        self.solutions.write("Time,Checks,Solution\n")
        timestamp = datetime.datetime.now().strftime(LOG_TIMESTAMP)
        output = "{0},1,{1}\n".format(timestamp, solution)
           
        self.solutions.write(output)
        self.logger.info("First Candidate: {0}".format(solution))
        for temperature in self.temperatures:
            if self.stop_condition(self.solution):
                self.logger.info('Stop condition reached with solution: {0}'.format(self.solution))
                break

            self.logger.debug("Temperature: {0}".format(temperature))
            candidate = self.tweak(solution)

            # this needs to be smarter -- what if the space is exhausted?
            self.logger.debug("Searching for a candidate not in the tabu space")
            while str(candidate.inputs) in self.tabu and not self.stop_condition(self.solution):
                candidate = self.tweak(solution)

            self.logger.debug("Trying candidate: {0}".format(candidate))

            quality_difference = self.quality(candidate) - self.quality(solution)
            
            # since the candidate is checked to see if it's in the tabu list
            # before checking its quality, only the inputs are added to the tabu list
            self.tabu.append(str(candidate.inputs))
            
            if (quality_difference > 0 or
                random.random() < math.exp(quality_difference/float(temperature))):
                solution = candidate
                self.logger.info("Candidate '{0}' new local solution".format(solution))
            if self.quality(solution) > self.quality(self.solution):
                timestamp = datetime.datetime.now().strftime(LOG_TIMESTAMP)
                output = "{0},{1},{2}\n".format(timestamp, self.quality.quality_checks, solution)
                self.solutions.write(output)
                self.logger.info("New Best Solution: {0}".format(output))
                self.solution = solution
        self.logger.info("Quality Checks: {0} Solution: {1} ".format(self.quality.quality_checks,
                                                                     self.solution))
        if self.observers is not None:
            # this is for users of the solution
            self.observers(solution=self.solution)
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


if __name__ == '__builtin__':
    # third-party
    import matplotlib.pyplot as plt
    import numpy

    output = 'figures/geometric_plot.png'
    alpha = 0.99
    a2 = 0.95

    t_0 = 1000
    t = numpy.arange(t_0, 0, -1)
    y = t_0 * alpha**t
    y2 = t_0 * a2**t

    figure = plt.figure()
    axe = figure.gca()
    axe.plot(t, y, label='alpha=0.99')
    axe.plot(t, y2, label='alpha=0.95')

    axe.set_xlabel('Time')
    axe.set_ylabel("Temperature")
    axe.legend()
    figure.savefig(output)
    print ".. figure:: " + output


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
        self.__iter__().close()
        self.time = -1

    def reset(self):
        """
        Does the same thing as close
        """
        self.__iter__().close()
        self.time = -1


    def __str__(self):
        return "Start: {0}, Stop: {1}, Alpha: {2}, Current Time: {3}".format(self.start,
                                                                             self.stop,
                                                                             self.alpha,
                                                                             self.time)
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
