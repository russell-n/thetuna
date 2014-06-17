
# python standard library
from collections import OrderedDict
import os.path
from types import StringType, IntType

# third party
import numpy

# tuna
from component import BaseComponent
from tuna import ConfigurationError
from tuna.plugins.base_plugin import BasePlugin


class XYDataConstants(object):
    """
    Constants for builders of the XYData class
    """
    __slots__ = ()
    filename_option = 'filename'
    delimiter_option = 'delimiter'
    skiprows_option = 'skiprows'
    usecols_option = 'usecols'


CONFIGURATION = """
[XYData]
# this follows the pattern for plugins --
# the header has to match what's in the Optimizers `components` list
# the component option has to be XYData
component = XYData

# filename is required, everything else has defaults
filename = <path to data file>
delimiter = <column separator (default= ',')
skiprows = <number of rows to skip (default=0)
usecols = <index-list of columns to use (default=all)>
"""

DESCRIPTION = """
The XYData component is a stand-in that converts a delimited file to a numpy array. It is meant to be used as a `quality` measurement class so expects its calls to be passed an object with `inputs` and `output` attributes. It will look up the value in the array using the `inputs` value (so they have to be valid x and y indices) and set the output.  It also keeps a `quality_checks` attribute that is incremented for each call so the number of checks can be measured to estimate how long the optimizer would run if it were exploring the space that created the data set using an actual call to get the output (e.g. how many calls to iperf the optimizer would make).
"""


class XYDataQuality(BaseComponent):
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
        super(XYDataQuality, self).__init__()
        self.filename = filename
        self.delimiter = delimiter
        self.skiprows = skiprows
        self.usecols = usecols
        self.quality_checks = 0
        self.configuration = CONFIGURATION
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

    def __call__(self, target):
        """
        Main interface, sets the target.output value, increments self.quality_checks

        :param:

         - `target`: object with  with <x-index, y-index> for `input` attribute`

        :return: value from data at coordinates
        """
        self.quality_checks += 1
        if target.output is None:
            target.output = self.data[target.inputs[0], target.inputs[1]]
        return target.output

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
        """
        logs the number of quality-check- made and calls reset()
        """
        self.logger.info("Quality Checks: {0}".format(self.quality_checks))
        self.reset()
        return

    def reset(self):
        """
        Resets the quality_checks to 0
        """
        self.logger.info("Quality Checks: {0}".format(self.quality_checks))
        self.quality_checks = 0
        return
# end XYData    


class XYData(BasePlugin):
    """
    Builds XYData objects from configuration-maps
    """
    def __init__(self, *args, **kwargs):
        """
        XYDataBuilder constructor

        :param:

         - `configuration`: configuration map
         - `section`: name of section with needed options
        """
        super(XYData, self).__init__(*args, **kwargs)
        return

    @property
    def product(self):
        """
        A built XYData object
        """
        if self._product is None:
            filename = self.configuration.get(section=self.section_header,
                                              option=XYDataConstants.filename_option,
                                              optional=False)
            delimiter = self.configuration.get(section=self.section_header,
                                               option=XYDataConstants.delimiter_option,
                                               optional=True,
                                               default=',')
            skiprows = self.configuration.get_int(section=self.section_header,
                                                  option=XYDataConstants.skiprows_option,
                                                  optional=True,
                                                  default=0)
            usecols = self.configuration.get_list(section=self.section_header,
                                                  option=XYDataConstants.usecols_option,
                                                  optional=True)
            if usecols is not None:
                usecols = [int(item) for item in usecols]
            self._product = XYDataQuality(filename=filename,
                                   delimiter=delimiter,
                                   skiprows=skiprows,
                                   usecols=usecols)
        return self._product

    @property
    def sections(self):
        """
        An ordered dictionary for the HelpPage
        """
        if self._sections is None:
            bold = '{bold}'
            reset = '{reset}'
            name = 'XYData'
            bold_name = bold + name + reset

            self._sections = OrderedDict()
            self._sections['Name'] = '{blue}' + name + reset + ' -- A component for optimizer plugins'
            self._sections['Description'] = bold_name + DESCRIPTION
            self._sections["Configuration"] = CONFIGURATION
            self._sections['Files'] = __file__
        return self._sections

    def fetch_config(self):
        """
        prints sample configuration to the scree
        """
        print CONFIGURATION
        return

