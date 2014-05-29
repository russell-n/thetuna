
# python standard library
import unittest

# this package
from optimization.simulations.normalsimulation import NormalSimulation


class TestNormalSimulation(unittest.TestCase):
    def test_constructor(self):
        """
        Does it build?
        """
        simulator = NormalSimulation(domain_start=-4, domain_end=4, domain_step=0.1)
        self.assertEqual(simulator.ideal_solution, simulator.range.max())
        return
