The Base Plugin
===============
.. currentmodule:: tuna.plugins.base_plugin


.. _base-plugin:

Background
----------

This module contains a `BasePlugin` class that forms the foundation of the `ape` plugin-system. Creating a `BasePlugin` makes it easier to add code as it provides a concrete target for the person adding the code, removes the need for the infrastructure code to be changed when plugins are added, and encourages documentation by providing a built-in online help-interface and auto-included `rst` files.

In order to create a child of the `BasePlugin` you are required to implement two properties and one method: ``sections``, ``product``, and ``fetch_config()``. The ``sections`` and ``fetch_config`` are for the user-interface while the ``product`` should be the object to run. The ``sections`` can be ``None`` if you do not want the online help, but should otherwise be a dictionary with section-names as keys and content-strings as values. It will be passed to the :ref:`HelpPage <help-page>` so you should see that if you want to know what will be done with the ``sections`` property. If the ordering is important use a ``collections.OrderedDict``. The
``fetch_config`` is expected to be a method that sends a sample config-file snippet to stdout. I chose stdout rather than to disk because it allows the user to append it to existing files using redirection ``>>`` and it also serves as a prompt for those who just need to remember what the configuration should look like (I also had problems with users accidentally clobbering their configurations by pulling sample files). The ``product`` should be the built-object for the code to run (only the ``__call__`` method will be used so that has to be implemented on the ``product``). When the child-plugin is implemented, it will be passed a :ref:`ConfigurationMap <configuration-map>` that will provide data-types pulled from whatever configuration file it was given for the plugin to use in configuring the product.

The :ref:`QuarterMaster <quarter-master>` looks for child-classes of the `BasePlugin` when deciding what is a valid plugin, so besides defining an implementation expectation for the new plugin, the `BasePlugin` also provides the means for inclusion in the `ape` (even if you drop a module in this folder, if nothing in it is a child of the `BasePlugin` it will be ignored). To check if it contains a `BasePlugin` the module has to be imported so be careful with globals and imports.

The `BasePlugin` class and the ``plugins`` package also provides the foundation for user help. As noted above, the ``sections`` and ``fetch_config`` are meant for online help and in addition to this the ``index.pnw`` file contains code to include any ``rst`` files in the ``plugins`` directory so adding documentation files here will add the text to the documentation when it is regenerated::

   Pweave index.pnw

To summarize, the `BasePlugin` is the main way to add code that will be exposed to the end user.

.. warning:: I have had a lot of problems troubleshooting when I accidentally name plugin-class the same thing as (one of) the class(es) it's building -- the re-definition of the name will wipe out your imported name. Don't do it. (e.g. don't create a plugin named Sample that builds a class named Sample as its product.)

.. '

Class Diagram
-------------

This is an (idealized) class diagram (see below for an auto-generated one).
    
.. uml::

   BaseClass <|-- BasePlugin
   BaseClass : logger
   BasePlugin : configuration
   BasePlugin o- HelpPage
   BasePlugin : sections
   BasePlugin : product
   BasePlugin : help(width)
   BasePlugin : fetch_config()
   BasePlugin : section_header

Public Properties and Methods
-----------------------------

The following are the public propeties and methods. The ``help_page`` and ``help()`` are the only implemented attributes, the rest need to be implemented by the inheriting classes.

.. _base-plugin-sections:
Sections
~~~~~~~~

The `sections` are a dictionary used by the help-page to create the screen-output. By defining this dictionary you are defining what the user will see when they enter::

    ape help <plugin-name>

.. _base-plugin-product:
The Product
~~~~~~~~~~~

This is the built object that client code will call. To make the interface uniform it is assumed that all parameters have been set and none will be passed to the __call__() method.

.. _base-fetch-config::
The Fetch Config
~~~~~~~~~~~~~~~~

The `fetch_config` method used to copy an example configuration file to the current working directory (thus its name). Since each plugin can provide its own sample, I decided that they should instead output them to standard out. Thus the user could do something like this::

    ape fetch > ape.ini
    ape fetch IperfSession >> ape.ini

And so on to add to a configuration file without clobbering the old one. Additionally, the ConfigurationMap looks for a `config_glob` option in the APE section so the other configuration files could be put in a seaparate file and shared by other APE configurations.    
   
.. autosummary:: 
   :toctree: api

   BasePlugin
   BasePlugin.sections
   BasePlugin.help_page
   BasePlugin.help
   BasePlugin.product
   BasePlugin.fetch_config

Aggregated Classes
------------------

These are the classes that the BasePlugin uses.

.. currentmodule:: ape.commoncode.baseclass
.. autosummary::
   :toctree: api

   BaseClass.logger

.. currentmodule:: ape.parts.helppage.helppage
.. autosummary::
   :toctree: api

   HelpPage
   HelpPage.__call__
     


.. Module Graph
.. ------------
.. 
.. <<name='module_graph', echo=False, results='sphinx'>>=
.. if in_pweave:
..     from ape.plugins.base_plugin import BasePlugin
..     print "This is a module diagram for **{0}**.\n".format(BasePlugin.__module__)
..     this_file = os.path.join(os.getcwd(), 'base_plugin.py')
..     module_diagram_file = module_diagram(module=this_file, project='baseplugin')
..     print ".. image:: {0}".format(module_diagram_file)
.. 
.. 

.. Class Diagram
.. -------------
.. 
.. This is an auto-generated diagram of the BasePlugin class.
..     
.. <<name='class_diagram', echo=False, results='sphinx'>>=
.. if in_pweave:
..     class_diagram_file = class_diagram(class_name="BasePlugin",
..                                        filter='OTHER',
..                                        module=this_file)
..     print ".. image:: {0}".format(class_diagram_file)
.. 