
# python standard library
import re
import csv
import datetime
import socket
import textwrap
import os

# this package
from tuna import BaseClass
from tuna import TunaError
from tuna.clients.simpleclient import ConnectionError
from tuna.infrastructure.baseconfiguration import BaseConfiguration
from tuna.commands.command import TheCommand


TIMESTAMP = 'timestamp'
UNDERSCORE = '_'
ONE = 1
FIRST = 0
LAST = -1
APPENDABLE = 'a'
WRITEABLE = 'w'


class Query(BaseClass):
    """
    A querier of devices
    """
    def __init__(self, storage, output_filename, connection, fields, commands):
        """
        Query constructor

        :param:

         - `storage`: A file-like object to send the data to
         - `output_filename`: name of file to use to save data
         - `connection`: Connection to the DUT
         - `fields`: list of fields for headers (and keys to 'commands' dict)
         - `commands`: dict of field:command where commands are callable objects that
        """
        super(Query, self).__init__()
        self.storage = storage
        self._output_file = None
        self.output_filename = output_filename
        self.fields = fields
        self.commands = commands
        self.new_file = True
        self._writer = None
        return        

    @property
    def output_file(self):
        """
        Writeable output file for the DictWriter

        :postcondition:

          - self.output_file is opened file with new_filename
          - self._writer is None
          - self.new_file is False if the new_filename was an existing file

        :return: opened writeable file with self.output_filename as name
        """
        if self._output_file is None:
            # an ugly hack to let the writer know if this is a new file
            # because onec it's open, it will exist, even if not written to
            full_path = os.path.join(self.storage.path, self.output_filename)
            self.new_file = not os.path.isfile(full_path)
            self._output_file = self.storage.open(self.output_filename,
                                                  mode=APPENDABLE)
            self._writer = None
        return self._output_file

    @property
    def writer(self):
        """
        A DictWriter that writes the query data to a csv-file

        :precondition:

         - `self.output_file` is an opened writeable file
         - `self.new_file` is True if the opened file didn't exist before opening
         
        :postcondition:

         - self.writer is DictWriter
         - self.fields written as header
        """
        if self._writer is None:
           self._writer =  csv.DictWriter(self.output_file,
                                          fieldnames=[TIMESTAMP]  + self.fields)

           if self.new_file:
               self._writer.writeheader()
        return self._writer

    def close(self):
        """
        Closes the output-file
        """
        self.output_file.close()
        return

    def __call__(self, extra_data=None):
        """
        The main interface, traverses commands and saves output to csv

        :param:

         - `extra_data`: extra data to add to the csv (keys have to already be added to the `fields` list)

        :raise: CameraobscuraError if the regular expressions matches but there's no group
        """
        output = {TIMESTAMP:datetime.datetime.now().isoformat()}
        if extra_data is not None:
            output.update(extra_data)
                
        for field, command in self.commands.iteritems():
            self.logger.debug("Checking field {0}".format(field))
            output[field] = command()

        self.logger.info(output)
        self.writer.writerow(output)
        return

    def check_rep(self):
        """
        Checks that
           * commands and expressions have the same keys
           * keys they are in fields list
           
        :raise: AssertionError if either is False
        """
        for key in self.commands.iterkeys():
            assert key in self.fields, "Extra key in 'commands': {0}".format(key)
        return
    
    def __del__(self):
        """
        Closes the file
        """
        self.close()
        return
# end Query    


class QueryEnum(object):
    __slots__ = ()
    section = 'query'

    # special options
    delimiter = 'delimiter'
    not_available = 'not_available'
    filename = 'filename'
    timeout = 'timeout'
    trap_errors = 'trap_errors'
    connection = 'connection'
    plugin = 'plugin'
    component = 'component'

    # reserved names
    reserved = [delimiter, not_available, filename, timeout,
                trap_errors, connection, plugin, component]
    
    # defaults
    default_delimiter = ','
    default_not_available = 'NA'
    default_filename = 'query.csv'
    default_timeout = 10
    default_trap_errors = True


class QueryConfiguration(BaseConfiguration):
    """
    A holder of query configurations
    """
    def __init__(self, section=None, *args, **kwargs):
        """
        QueryConfiguration constructor

        :param:

         - `section`: section-name in the configuration
        """
        super(QueryConfiguration, self).__init__(*args, **kwargs)
        self._section = section
        self._fields = None
        self._delimiter = None
        self._not_available = None
        self._commands = None
        self._expressions = None
        self._filename = None
        self._timeout = None
        self._trap_errors = None
        return

    @property
    def example(self):
        """
        An example query configuration
        """
        if self._example is None:
            self._example = textwrap.dedent("""
            #[{section}]
            # these are arbitrary commands that will be called in between attenuations
            # it's original use-case is to get RSSI and other monitoring information
            # but since it's free-form you can pass in whatever you like
            
            # delimiter separating command and expression
            # this is provided so that if the command or expression has a comma in it
            # you can use an alternative
            
            #delimiter =  {delimiter}

            # if you want to specify a filename set the filename option
            # filename = {filename}

            # to change the readline timeout
            # timeout = {timeout}

            # to have it crash instead of trap socket errors
            # trap_errors = {trap_errors}

            # everything else is of the format:
            # <column-header> = <command><delimiter><regular expression>
            # the column-header will be used in the csv-file
            # the regular expression has to have a group '()' or it will raise an error
            
            #rssi = iwconfig wlan0,Signal\slevel=(-\d+\sdBm)
            #noise = wl noise, (.*)
            #bitrate = iwconfig wlan0, Bit\sRate=(\d+\.\d\sMb/s)
            #counters = wl counters, (rxcrsglitch [0-9]* )
            """.format(section=self.section,
                       delimiter=QueryEnum.default_delimiter,
                       timeout=QueryEnum.default_timeout,
                       filename=QueryEnum.default_filename,
                       trap_errors=QueryEnum.trap_errors))
        return self._example
    
    @property
    def section(self):
        """
        The configuration section name
        """
        if self._section is None:
            self._section = QueryEnum.section
        return self._section

    @property
    def delimiter(self):
        """
        The delimiter separating the <command> and <expression> for each field.

        :return: string used to separate the sub-values `command` and `expression`
        """
        if self._delimiter == None:
            self._delimiter = self.configuration.get(section=self.section,
                                                     option=QueryEnum.delimiter,
                                                     optional=True,
                                                     default=QueryEnum.default_delimiter)
        return self._delimiter

    @property
    def not_available(self):
        """
        The symbol to use if the command fails to retrieve a value.

        :default: NA
        """
        if self._not_available is None:
            self._not_available = self.configuration.get(self.section,
                                                         QueryEnum.not_available,
                                                         optional=True,
                                                         default=QueryEnum.default_not_available)
        return self._not_available

    @property
    def fields(self):
        """
        List of field names (options from the section) for commands
        """
        if self._fields is None:
            defaults = self.configuration.defaults.keys()
            options = self.configuration.options(self.section)

            excluded =  defaults + QueryEnum.reserved
            self._fields = [option for option in options
                            if option not in excluded]
        return self._fields

    @property
    def commands(self):
        """
        Dictionary of field:command
        """
        if self._commands is None:
            # commands is a generator of first-entries in the values split by the delimiter
            # e.g. field = command,expression

            commands = (self.configuration.get(self.section, option).split(self.delimiter, ONE)[FIRST] for option in self.fields)
            
            self._commands = dict(zip(self.fields, commands))
        return self._commands

    @property
    def expressions(self):
        """
        Dictionary of field:expression

        This strips off whitespace from the ends to avoid introducing unexpected spaces
        """
        if self._expressions is None:
            # expressions are the leftovers after the command is extracted from the values
            expressions = (self.configuration.get(self.section, option).split(self.delimiter, ONE)[LAST].strip() for option in self.fields)            
            self._expressions = dict(zip(self.fields, expressions))
        return self._expressions

    @property
    def filename(self):
        """
        The name of a file to use for the csv data        
        """
        if self._filename is None:
            self._filename = self.configuration.get(self.section,
                                                    QueryEnum.filename,
                                                    optional=True,
                                                    default=QueryEnum.default_filename)
        return self._filename

    @property
    def timeout(self):
        """
        Readline timeout
        """
        if self._timeout is None:
            self._timeout = self.configuration.getfloat(self.section,
                                                        QueryEnum.timeout,
                                                        optional=True,
                                                        default=QueryEnum.default_timeout)
        return self._timeout

    @property
    def trap_errors(self):
        """
        Boolean to decide whether or not to trap errors
        """
        if self._trap_errors is None:
            self._trap_errors = self.configuration.getboolean(self.section,
                                                           QueryEnum.trap_errors,
                optional=True,
                default=QueryEnum.default_trap_errors)
        return self._trap_errors

    def reset(self):
        """
        Resets the options to None
        """
        self._filename = None
        self._commands = None
        self._expressions = None
        self._delimiter = None
        self._not_available = None
        return        
        
    def check_rep(self):
        """
        Checks the representation

        :raises: AssertionError if there is an invalid option
        """
        super(QueryConfiguration, self).check_rep()
        return
# end class QueryConfiguration    


class QueryBuilder(object):
    """
    A builder of queries
    """
    def __init__(self, connection, configuration, storage):
        """
        QueryBuilder Constructor

        :param:

         - `connection`: Connection to the device to query
         - `configuration`: built QueryConfiguration
         - `storage`: file-like object for data
        """
        self.connection = connection
        self.configuration = configuration
        self.storage = storage
        self._product = None
        self._commands = None
        return

    @property
    def commands(self):
        """
        A dict of TheCommand objects built from the configuration and connection
        """
        if self._commands is None:
            commands = [TheCommand(connection=self.connection,
                                   command=self.configuration.commands[field],
                                   data_expression=self.configuration.expressions[field],
                                   identifier=field,
                                   timeout=self.configuration.timeout,
                                   trap_errors=self.configuration.trap_errors)
                                   for field in self.configuration.fields]
            self._commands = dict(zip(self.configuration.fields,
                                      commands))
        return self._commands

    @property
    def product(self):
        """
        Query built from the connection and configuration
        """
        if self._product is None:
            self._product = Query(output_filename=self.configuration.filename,
                                  storage=self.storage,
                                  connection=self.connection,
                                  fields=self.configuration.fields[:],
                                  commands=self.commands)
        return self._product        
# end QueryBuilder                
