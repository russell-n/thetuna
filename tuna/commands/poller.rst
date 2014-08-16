The Poller Class
================

.. _poller-class:

To accomodate the almost arbitrary ways to get device-state information from a DUT, a general `Poller` class is created to let user's specify commands to send and expressions to extract information from their output. This is related to the :ref:`Query <query-class>` but is intended to run continuously, calling the command(s) at periodic intervals.

.. '



The Poller Class
---------------

.. uml::

   BaseClass <|-- Poller
   Poller : File output_file
   Poller : SSHClient connection   
   Poller : List fields
   Poller : Dict commands
   Poller : Dict expressions
   Poller : DictWriter writer
   Poller : String not_available
   Poller : __call__()
   Poller o- csv.DictWriter
   Poller o- client
   Poller o- TheCommand

.. module:: tuna.commands.poller
.. autosummary::
   :toctree: api

   Poller
   Poller.timer
   Poller.output_file
   Poller.writer
   Poller.close
   Poller.run_once
   Poller.run
   Poller.__call__
   Poller.check_rep
   Poller.__del__

The Run
--------

The `run_once` method builds a dictionary of data output from the Poller's commands. It always starts with a timestamp  before calling each command. After calling each command once it writes the output as a row in the (csv) output-file.

.. '

::

    class PollerEnum(object):
        __slots__ = ()
        # special options
        delimiter = 'delimiter'
        interval = 'interval'
        not_available = 'not_available'
        filename = 'filename'
        trap_errors = 'trap_errors'
        connection = 'connection'
        plugin = 'plugin'
        component = 'component'
        timeout = 'timeout'
    
        # reserved names
        reserved = [delimiter, not_available, filename, timeout,
                    interval, timeout,
                    trap_errors, connection, plugin, component]
        
        # defaults
        default_delimiter = ','
        default_not_available = 'NA'
        default_filename = 'poller_data.csv'
        default_interval = 1
        default_trap_errors = True
        default_timeout = 10
    
    




.. _poller-configuration:

The PollerConfiguration
----------------------

.. uml::

   BaseConfiguration <|-- PollerConfiguration
   PollerConfiguration : String delimiter
   PollerConfiguration : List fields
   PollerConfiguration : List commands
   
.. module:: tuna.commands.poller
.. autosummary::
   :toctree: api

   PollerConfiguration
   PollerConfiguration.delimiter
   PollerConfiguration.interval
   PollerConfiguration.not_available
   PollerConfiguration.fields
   PollerConfiguration.commands
   PollerConfiguration.expressions
   PollerConfiguration.filename
   PollerConfiguration.timeout


.. csv-table:: PollerConfiguration defaults
   :header: value, default
   :delim: ;

   delimiter;,
   not_available; NA
   interval; 1 Second
   filename; query.csv
   timout; 10 Seconds

Example Configuration
---------------------

::

    EXAMPLE_CONFIGURATION = """
    #[poller]
    # these are arbitrary commands that will be called in a thread
    # it's original use-case is to get RSSI and other monitoring information
    # but since it's free-form you can pass in whatever you like
                
    # delimiter separating command and expression
    # this is provided so that if the command or expression has a comma in it
    # you can use an alternative
                
    #delimiter =  {delimiter}
    
    # the interval is the amount of time between calling the commands
    # if it's longer than a minute you can use words (e.g. day, hour)
    # but not months (that's too hard to calculate) if you don't use a
    # word it's assumed to be seconds
    # interval = {interval}
    
    # the timeout is the readline timeout
    
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
    #
    
    #rssi = iwconfig wlan0,Signal\slevel=(-\d+\sdBm)
    #noise = wl noise, (.*)
    #bitrate = iwconfig wlan0, Bit\sRate=(\d+\.\d\sMb/s)
    #counters = wl counters, (rxcrsglitch [0-9]* )
    """.format(delimiter=PollerEnum.default_delimiter,
               timeout=PollerEnum.default_timeout,
               filename=PollerEnum.default_filename,
               trap_errors=PollerEnum.default_trap_errors,
               interval=PollerEnum.default_interval)
    
    
    



The Poller Builder
------------------

This is a first builder. The intent is that for each high-level component there will be a `Class - Configuration - Builder` troika. Each builder should know how to build its object, but defer to another builder if it needs something that is not unique to it.

    * Configurations map config-files to parameters needed to build a component
    * Builders map configurations and built-objects to built components

.. uml::

   PollerBuilder : ThePoller product
   PollerBuilder : TheHost connection
   PollerBuilder : PollerConfiguration configuration
    
.. autosummary::
   :toctree: api

   PollerBuilder
   PollerBuilder.product

