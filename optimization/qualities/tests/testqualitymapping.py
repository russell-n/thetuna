
# python standard library
import unittest
import random

# third-party
from mock import MagicMock
import numpy

# this package
from optimization.qualities.qualitymapping import QualityMapping


class TestQualityMapping(unittest.TestCase):
    def setUp(self):
        self.domain = MagicMock()
        self.mapping_function = MagicMock()
        self.ideal = random.randrange(100)
        self.maxima = random.choice((True, False))
        self.mapping = QualityMapping(mapping=self.mapping_function,
                                      domain=self.domain,
                                      ideal=self.ideal,
                                      maxima=self.maxima)
        return
    
    def test_constructor(self):
        """
        Does it build as expected?
        """
        self.assertEqual(self.domain, self.mapping.domain)
        self.assertEqual(self.mapping_function, self.mapping.mapping)
        self.assertEqual(self.ideal, self.mapping.ideal)
        self.assertEqual(self.maxima, self.mapping.maxima)
        return

    def test_ideal(self):
        """
        Does it get the ideal solution correctly?
        """
        # base-case, user set it
        self.assertEqual(self.mapping.ideal, self.ideal)

        # user doesn't set it and doesn't set the domain either
        self.mapping.ideal = None
        self.mapping.domain = None
        self.assertIsNone(self.mapping.ideal)

        # user doesn't set the ideal but does set the domain
        self.mapping.domain = numpy.array(range(5))
        self.mapping.mapping = lambda x: x**2
        self.mapping.maxima = True
        self.assertEqual(16, self.mapping.ideal)

        # test the minima
        self.mapping.maxima = False
        self.mapping.ideal = None
        self.assertEqual(0, self.mapping.ideal)

        # user sets both the domain and the ideal
        # take the user-setting, not a calculated value
        expected = random.randrange(6, 100)
        self.mapping.ideal = expected
        self.assertEqual(expected, self.mapping.ideal)
        return

    def test_call(self):
        """
        Does the call map an input to an output?
        """
        argument = random.randrange(-100, 100)
        mock_argument = MagicMock()
        mock_argument.input = argument
        output = random.randrange(-100, 100)
        mock_argument.output = output
        self.mapping_function.return_value = mock_argument

        value = self.mapping(mock_argument)
        self.assertEqual(output, value)        
        return
# end TestQualityMapping    
