
# python standard library
import os.path
from types import StringType, IntType

# third party
import numpy

# tuna
from component import BaseComponent
from tuna import ConfigurationError


class XYData(BaseComponent):
    """
    A csv-file to quality-value translator
    """
    def __init__(self, filename, delimiter=',', skiprows=0,
                 usecols=None):
        """
        XYData Constructor

        :param:

         - `filename`: name of csv-file
         - `delimiter`: column separator
         - `skiprows`: number of rows in file to skip
         - `usecols`: specific columns to use         
        """
        self.filename = filename
        self.delimiter = delimiter
        self.skiprows = skiprows
        self.usecols = usecols
        self._data = None
        return

    @property
    def data(self):
        """
        numpy array built from the csv-file
        """
        if self._data is None:
            self._data = numpy.loadtxt(self.filename,
                                       delimiter=self.delimiter,
                                       skiprows=self.skiprows,
                                       usecols=self.usecols)
        return self._data

    def __call__(self, coordinates):
        """
        Main interface

        :param:

         - `coordinates`: collection with <x-index, y-index> for data

        :return: value from data at coordinates
        """        
        return self.data[coordinates[0], coordinates[1]]

    def check_rep(self):
        """
        Checks the flie parameters
        """
        if not os.path.isfile(self.filename):
            raise ConfigurationError("'{0}' is not a valid filename".format(self.filename))
        if not type(self.delimiter) is StringType:
            raise ConfigurationError("'{0}' is not a valid delimiter".format(self.delimiter))
        if not type(self.skiprows) is IntType:
            raise ConfigurationError("'{0}' is not a valid skiprows value".format(self.skiprows))
        return

    def close(self):
        return
# end XYData    
