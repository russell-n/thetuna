
# python standard library
import unittest
import random

# third-party
from mock import MagicMock

# this package
from optimization.optimizers.simulatedannealing import SimulatedAnnealing
from optimization.optimizers.simulatedannealing import TemperatureGenerator


class TestSimulatedAnnealing(unittest.TestCase):
    def setUp(self):
        self.candidates = MagicMock()
        self.temperature_schedule = MagicMock()
        self.quality = MagicMock()
        self.candidate = MagicMock()
        self.optimizer = SimulatedAnnealing(temperature_schedule=self.temperature_schedule,
                                            candidates=self.candidates,
                                            candidate=self.candidate,
                                            quality=self.quality)
        return
    
    def test_constructor(self):
        """
        Does it build?
        """
        self.assertEqual(self.temperature_schedule,
                         self.optimizer.temperature_schedule)
        self.assertEqual(self.candidates,
                         self.optimizer.candidates)
        self.assertEqual(self.quality,
                         self.optimizer.quality)
        self.assertEqual(self.candidate,
                         self.optimizer.candidate)
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
