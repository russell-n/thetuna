
# python standard library
import unittest
import random

# third party
import numpy

# this package
from optimization.simulations.basesimulation import BaseSimulation


class TestBaseSimulation(unittest.TestCase):
    def setUp(self):
        self.start_x = random.randrange(10)
        self.end_x = random.randrange(11, 100)
        self.step_size = random.random()
        self.expected = numpy.arange(self.start_x,
                                     self.end_x+self.step_size,
                                     self.step_size)
        self.simulator = BaseSimulation(self.start_x,
                                        self.end_x,
                                        self.step_size)
        return
    
    def test_constructor(self):
        """
        Does it build?
        """
        start_x = 0
        end_x = 100
        step_size = 0.1
        simulator = BaseSimulation(domain_start=start_x, domain_end=end_x,
                                   domain_step=step_size)
        self.assertEqual(start_x, simulator.domain_start)
        self.assertEqual(end_x, simulator.domain_end)
        self.assertEqual(step_size, simulator.domain_step)
        expected = numpy.arange(start_x, end_x + step_size, step_size)
        self.assertTrue(all(expected == simulator.domain))
        return

    def test_index(self):
        """
        Does it get the index of the nearest value in X?
        """
        target = random.randrange(50) + random.random()
        for index, value in enumerate(self.expected):
            if target <= value:
                break
        self.assertEqual(index, self.simulator.nearest_index(target)) 
        return
# end TestBaseSimulation    
