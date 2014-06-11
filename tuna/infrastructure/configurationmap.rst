The Configuration Map
=====================

.. _configuration-map:

The `Configuration Map` maps a configuration-file-name to data. It extends the `ConfigParser` to have more data-types (and allow missing values) and to add sub-configuration-files (see the :ref:`ConfigParser Explorations <exploring-configparser-whole-shebang>` to get some idea of what I am getting at).

Contents:

    * :ref:`Background <configurationmap-background>`

    * :ref:`UML Class Diagram <configurationmap-uml>`

    * :ref:`ConfigurationError <configurationmap-configurationerror>`

    * :ref:`The API <configurationmap-api>`

    * :ref:`The ConfigurationMap Parser <configurationmap-parser>`

    * :ref:`The ConfigParser <configurationmap-configparser>`

    * :ref:`ConfigParser Exceptions <configurationmap-exceptions>`

    * :ref:`Module Diagram <configurationmap-module-diagram>`

    * :ref:`Class Implementation Diagram <configurationmap-class-implementation-diagram>`

.. _configurationmap-background:    
    
Background
----------

The `ConfigParser` module along with the `glob` module will be used to find and convert files to data. The ConfigParser has methods for the main singular data-types but I will also add collections and times. Additionally I will automatically add any sub-config files matching a `config_glob` found in the DEFAULT section of the main file given. I am also setting the `allow_no_value` option to True so that you can use options without values::

    [SECTION]
    option = value
    valueless_option



.. _configurationmap-uml:

UML Model
---------

.. uml::

   ConfigurationMap -|> BaseClass
   ConfigurationMap o- ConfigParser

.. _configurationmap-configurationerror:   

The ConfigurationError
----------------------

The `ConfigurationMap` will raise a ConfigurationError to try and trickle up more useful information.

.. currentmodule:: tuna
.. autosummary::
   :toctree: api

   ConfigurationError



.. _configurationmap-api:

The API
-------

.. currentmodule:: tuna.infrastructure.configurationmap
.. autosummary::
   :toctree: api

   ConfigurationMap
   ConfigurationMap.get
   ConfigurationMap.get_type
   ConfigurationMap.get_int
   ConfigurationMap.get_float
   ConfigurationMap.get_boolean
   ConfigurationMap.get_relativetime
   ConfigurationMap.get_datetime
   ConfigurationMap.get_list
   ConfigurationMap.get_dictionary
   ConfigurationMap.get_ordered_dictionary
   ConfigurationMap.get_named_tuple
   ConfigurationMap.sections
   ConfigurationMap.has_option
   ConfigurationMap.options
   ConfigurationMap.items
   ConfigurationMap.defaults
   ConfigurationMap.write

.. note:: get_relativetime and get_absolutetime are currently using the defaults. If more control is needed, you will need to grab the option and build them yourself.
   
.. _configurationmap-parser:   

The ConfigurationMap.parser
---------------------------

This property is a SafeConfigParser instance. When it is created, the ConfigurationMap reads the filename passed in on instantiation and checks if the loaded configuration has a ``[DEFAULT] : config_glob`` option. If it does, it gets the `config_glob` value, traverses the expanded glob and loads all the files that match.

.. _configurationmap-configparser:

ConfigParser
------------

These are the `ConfigParser` methods that will be used.

.. currentmodule:: ConfigParser
.. autosummary::
   :toctree: api

   SafeConfigParser
   SafeConfigParser.options
   SafeConfigParser.sections
   SafeConfigParser.items
   SafeConfigParser.read
   SafeConfigParser.write
   SafeConfigParser.get
   SafeConfigParser.getint
   SafeConfigParser.getfloat
   SafeConfigParser.getboolean
   SafeConfigParser.has_option
   SafeConfigParser.has_section

.. _configurationmap-exceptions:
   
ConfigParser Exceptions
-----------------------

These are the `ConfigParser` Exceptions that I will handle in the `ConfigurationMap`.

.. currentmodule:: ConfigParser
.. autosummary::
   :toctree: api

   ConfigParser.Error
   ConfigParser.NoSectionError
   ConfigParser.NoOptionError

