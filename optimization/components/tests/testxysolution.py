
# python standard library
import unittest
import random

# third-party
import numpy

# this package
from optimization.components.xysolution import XYSolution


class TestXYSolution(unittest.TestCase):
    def setUp(self):
        self.x = numpy.array([random.randrange(10)])
        self.y = random.randrange(10)
        self.solution = XYSolution(inputs=self.x,
                                   output=self.y)
        return
    
    def test_constructor(self):
        """
        Does it build correctly?
        """
        self.assertEqual(self.x, self.solution.inputs)
        self.assertEqual(self.y, self.solution.output)
        return

    def test_equality(self):
        """
        Does it test if two outputs are equal?
        """
        solution_2 = XYSolution(None, self.y)
        self.assertEqual(solution_2, self.solution)

        solution_2.output = self.y + 1
        self.assertNotEqual(solution_2, self.solution)
        return

    def test_add(self):
        """
        Does it add arrays to the inputs?
        """
        tweak = numpy.array([1])
        summand = self.solution + tweak
        self.assertEqual(self.solution.inputs + 1, summand)

        summand = tweak + self.solution
        self.assertEqual(self.solution.inputs + 1, summand)
        return

    def test_subtract(self):
        """
        Does it subtract?
        """
        tweak = numpy.array([1])
        difference = self.solution - tweak
        self.assertEqual(difference, self.solution.inputs - tweak)

        difference = tweak - self.solution
        self.assertEqual(difference, tweak - self.solution.inputs)
        return

    def test_length(self):
        """
        Does it return the length of the inputs as its length?
        """
        length = random.randrange(2, 20)
        self.solution.inputs = range(length)
        self.assertEqual(length, len(self.solution))
        return

    def test_multiply(self):
        """
        Does it multiply the inputs?
        """
        value = random.randrange(1, 20)
        outcome = self.solution * value
        self.assertEqual(outcome, self.solution.inputs * value)

        outcome = value * self.solution
        self.assertEqual(outcome, self.solution.inputs * value)
        return

    def test_less_than(self):
        """
        Does it make a < comparison?
        """
        value = random.randrange(1, 20)
        other = XYSolution(None, self.solution.output + value)
        self.assertTrue(self.solution < other)

        other = XYSolution(None, self.solution.output - value)
        self.assertTrue(other < self.solution)
        return

    def test_greater_than(self):
        """
        Does it make > comparisons?
        """
        other = XYSolution(None, self.solution.output + 1)
        self.assertTrue(other > self.solution)

        other.output = other.output - 2
        self.assertTrue(self.solution > other)
        return

    def test_greater_than_or_equal(self):
        """
        Does it make >= comparisons?
        """
        other = XYSolution(None, self.solution.output)
        self.assertTrue(other >= self.solution)
        other.output += 2
        self.assertTrue(other >= self.solution)
        self.assertFalse(other < self.solution)
        other.output -= 5

        self.assertTrue(other <=self.solution)
        self.assertTrue(self.solution >= other)
        
