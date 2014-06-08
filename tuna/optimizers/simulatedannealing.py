
# python standard library
import itertools
import random
import math


class SimulatedAnnealing(object):
    """
    a Simulated Annealing optimizer
    """
    def __init__(self, temperatures, candidates, quality, candidate):
        """
        SimulatedAnnealing Constructor

        :param:

         - `temperatures`: a generator of temperatures
         - `candidates`: a generator of candidate solutions
         - `quality`: Quality checker for candidates
         - `candidate`: initial candidate solution
        """
        self.temperatures = temperatures
        self.candidates = candidates
        self.quality = quality
        self.solution = candidate
        return

    def __call__(self):
        """
        Runs the optimization

        :return: last non-None output given
        """
        candidates_and_temperatures = itertools.izip(self.candidates,
                                                     self.temperatures)
        solution = self.solution
        for candidate, temperature in candidates_and_temperatures:
            quality_difference = self.quality(candidate) - self.quality(solution)
            if (quality_difference > 0 or
                random.random() < math.exp(quality_difference/float(temperature))):
                solution = candidate
            if self.quality(solution) > self.quality(self.solution):
                self.solution = solution
            print candidate, self.solution
        return self.solution
# SimulatedAnnealing    


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
