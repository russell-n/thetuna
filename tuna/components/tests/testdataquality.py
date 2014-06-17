
# python standard library
import unittest
import random

# third party
from mock import MagicMock, patch

# this package
from tuna.components.dataquality import XYData
from tuna import ConfigurationError


class TestXYData(unittest.TestCase):
    def setUp(self):        
        self.filename = 'aoesnuthlrcg'
        self.delimiter = 'rc'
        self.skiprows = random.randrange(100)
        self.usecols = (random.randrange(100))
        self.xy_data = XYData(filename=self.filename,
                              delimiter=self.delimiter,
                              skiprows=self.skiprows,
                              usecols=self.usecols)
        return
    
    def test_constructor(self):
        """
        Does it build correctly?
        """
        self.assertEqual(self.filename, self.xy_data.filename)
        self.assertEqual(self.delimiter,
                         self.xy_data.delimiter)
        self.assertEqual(self.skiprows,
                         self.xy_data.skiprows)
        self.assertEqual(self.usecols,
                         self.xy_data.usecols)
        return

    def test_defaults(self):
        """
        Does it have the expected defaults?
        """
        xy_data = XYData('aoesnthu')
        self.assertEqual(',', xy_data.delimiter)
        self.assertEqual(0, xy_data.skiprows)
        self.assertEqual(None, xy_data.usecols)
        return

    def test_data(self):
        """
        Does it build an array from the parameters given?
        """
        loader = MagicMock()
        with patch("numpy.loadtxt", loader):
            data = self.xy_data.data
            loader.assert_called_with(self.filename,
                                      delimiter=self.delimiter,
                                      skiprows=self.skiprows,
                                      usecols=self.usecols)
        return

    def test_call(self):
        """
        Does it get the value from the data?
        """
        class FakeData(object):
            def __init__(self, inputs):
                self.inputs = inputs
                self.output = None
            
        coordinates = [random.randrange(10), random.randrange(100)]
        input_output = FakeData(coordinates)
        output = random.randrange(100)
        loader = MagicMock()
        
        def getitem(*args):
            return output

        data = MagicMock()
        loader.return_value = data
        data.__getitem__.side_effect = getitem
        with patch("numpy.loadtxt", loader):
            actual = self.xy_data(input_output)
            self.assertEqual(actual, output)
            data.__getitem__.assert_called_with((coordinates[0],
                                                coordinates[1]))
        return

    def test_check_rep(self):
        """
        Does it check the file parameters?
        """
        path_mock = MagicMock()
        with patch('os.path.isfile', path_mock):
            self.xy_data.check_rep()
            path_mock.assert_called_with(self.filename)
            with self.assertRaises(ConfigurationError):
                path_mock.return_value = False
                self.xy_data.check_rep()
                path_mock.return_value = True
            with self.assertRaises(ConfigurationError):
                self.xy_data.delimiter = 1
                self.xy_data.check_rep()
                
            with self.assertRaises(ConfigurationError):
                path_mock.return_value = True
                self.xy_data.delimiter = ','
                self.xy_data.skiprows = None
                self.xy_data.check_rep()
        return
    
