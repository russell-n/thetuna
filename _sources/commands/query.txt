The Query Classes
===============

TheQuery
--------

.. _query-class:

To accomodate the almost arbitrary ways to get device-state information from a DUT, a general `Query` class is created to let user's specify commands to send and expressions to extract information from their output.

.. '



.. _query-class-responsibilities:

Responsibilities
----------------

   #. Maintains list of `fields` to use as headers for the files
   #. Maintains `commands` to send to the device 
   #. Maintains `expressions` (regular) to parse the output
   #. Maintains a csv-writer so save the output
   #. Maintains a connection to the device
   #. Traverses the fields, sending commands, checking output, and writing the results to the csv-writer
   
.. _query-class-collaborators:

Collaborators
-------------

    * csv.DictWriter
    * paramiko.SSHClient (or equivalent)

.. currentmodule:: csv
.. autosummary::
   :toctree: api

   csv.writer
   csv.DictWriter

.. module:: paramiko
.. autosummary::
   :toctree: api

   SSHClient

.. _query-class-path:

Main Path
---------

    1. Check if csv-output has been opened.
       1.1. Open csv-output if not opened
       1.2. Write header if output just opened
    2. Traverse fields
       2.1. Send field's command to connection
       2.2. traverse lines of output from connection
          2.2.1. check if field's expression matches line and add match to output-dictionary if it does
          2.2.2. If no match, continue to next line
       2.2. If no match made, add not-available token to output-dictionary
   3. Send output-dictionary to csv-output

.. figure:: figures/query_activity_diagram.svg
   :align: center

   Activity Diagram for Query call

.. _query-class-implementation:

The Query Class
---------------

.. uml::

   BaseClass <|-- Query
   Query : File output_file
   Query : SSHClient connection   
   Query : List fields
   Query : Dict commands
   Query : Dict expressions
   Query : DictWriter writer
   Query : String not_available
   Query : __call__()
   Query o- csv.DictWriter
   Query o- client
   Query o- TheCommand

.. module:: tuna.commands.query
.. autosummary::
   :toctree: api

   Query
   Query.output_file
   Query.writer
   Query.close
   Query.__call__
   Query.check_rep
   Query.__del__

The Call
--------

The call builds a dictionary of data output from the Query's commands. It always starts with a timestamp, then adds any 'extra_data' that was passed in to the call before calling each command. After calling each command once it writes the output as a row in the (csv) output-file.

.. '

::

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
    
    




.. _query-configuration:

The QueryConfiguration
----------------------

.. uml::

   BaseConfiguration <|-- QueryConfiguration
   QueryConfiguration : String delimiter
   QueryConfiguration : List fields
   QueryConfiguration : List commands
   
.. module:: tuna.commands.query
.. autosummary::
   :toctree: api

   QueryConfiguration
   QueryConfiguration.delimiter
   QueryConfiguration.not_available
   QueryConfiguration.fields
   QueryConfiguration.commands
   QueryConfiguration.expressions
   QueryConfiguration.filename

Example Configuration::

   [query]
   delimiter = ;
   not_available = nunya
   rssi = iwconfig wlan2; Signal\slevel=(-\d+\s+dBm)

.. csv-table:: QueryConfiguration defaults
   :header: value, default
   :delim: ;

   delimiter;,
   not_available; NA
   filename; query.csv
   



The Query Builder
-----------------

This is a first builder. The intent is that for each high-level component there will be a `Class - Configuration - Builder` troika. The configurations are already in place for most cases but the AutomatedRVR is this huge class, at least in part because it is acting as a builder of its parts as well as an executor of its test. As with the configurations it would be better to have an RVRBuilder (or some sensibly-named thing) and each part would have its own builder. This might not alway seem to be necessary, but in the case of things like TheCommand or TheQuery where they are expecting a connection to a remote device, it seems like there'd be too much redundant code to specify the connections every time. The Builder thus acts to defer the building of the components until the master-builder has built the connection. Each builder should know how to build its object, but defer to another builder if it needs something that is not unique to it.

    * Configurations map config-files to parameters needed to build a component
    * Builders map configurations and built-objects to built components

.. '

.. uml::

   QueryBuilder : TheQuery product
   QueryBuilder : TheHost connection
   QueryBuilder : QueryConfiguration configuration
    
.. autosummary::
   :toctree: api

   QueryBuilder
   QueryBuilder.product



The SummaryQuery
----------------

.. uml::

   Query <|-- SummaryQuery

