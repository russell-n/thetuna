
# python standard library
import unittest
import random

# third-party
from mock import MagicMock
import numpy

# this package
from tuna.optimizers.simulatedannealing import SimulatedAnnealer
from tuna.optimizers.simulatedannealing import TemperatureGenerator


class TestSimulatedAnnealing(unittest.TestCase):
    def setUp(self):
        self.candidates = MagicMock()
        self.temperature_schedule = MagicMock()
        self.quality = MagicMock()
        self.candidate = MagicMock()
        self.tweak = MagicMock()
        self.stop_condition = MagicMock()
        self.storage=MagicMock()
        self.optimizer = SimulatedAnnealer(temperatures=self.temperature_schedule,
                                            candidate=self.candidate,
                                            tweak=self.tweak,
                                            solution_storage=self.storage,
                                            stop_condition=self.stop_condition,
                                            quality=self.quality)
        return
    
    def test_constructor(self):
        """
        Does it build?
        """
        self.assertEqual(self.temperature_schedule,
                         self.optimizer.temperatures)
        self.assertEqual(self.quality,
                         self.optimizer.quality)
        self.assertEqual(self.candidate,
                         self.optimizer.solution)
        return

    def test_call(self):
        """
        Does it implement the simulated annealing algorithm?
        """
        self.optimizer.solution = 9
        qualities = dict(zip(xrange(10), reversed(xrange(10))))
        def quality_side_effect(value):
            return qualities[value]

        loops = 20
        candidates = numpy.random.choice(9, loops)
        self.optimizer.candidates = candidates
        self.optimizer.temperatures = numpy.random.choice(numpy.arange(1, 11), loops)
        self.quality.side_effect = quality_side_effect
        output = self.optimizer()
        self.assertEqual(len(self.quality.mock_calls), 4*loops)
        self.assertEqual(output, min(candidates))
        # actually testing the algorithm seems too hard, I'll do it empirically
        return


class TestTemperatureGenerator(unittest.TestCase):
    def setUp(self):
        self.start = 10
        self.stop = -2
        self.schedule = lambda x: x - 2
        self.generator = TemperatureGenerator(start=self.start,
                                              stop=self.stop,
                                              schedule=self.schedule)
        return
    
    def test_constructor(self):
        """
        Does it build?
        """
        self.assertEqual(self.start,
                         self.generator.start)
        self.assertEqual(self.stop,
                         self.generator.stop)
        self.assertEqual(self.schedule,
                         self.generator.schedule)
        return

    def test_schedule(self):
        """
        Do the schedules work as expected?
        """
        # just a sanity check
        temperature = random.randrange(100)
        generator = TemperatureGenerator(temperature)
        expected = temperature - 1        
        self.assertEqual(expected,
                         generator.schedule(temperature))
        self.assertEqual(expected-1,
                         self.generator.schedule(temperature))
        return

    def test_iterator(self):
        """
        Does it generate the values we expect?
        """
        expected = range(10, -4, -2)
        actual = [temperature for temperature in self.generator]
        self.assertEqual(expected, actual)
        return
