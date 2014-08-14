The QuarterMaster
=================

.. currentmodule:: tuna.infrastructure.quartermaster

The `QuarterMaster <http://en.wikipedia.org/wiki/Quartermaster>`_ handles finding and interacting with the plugins.



.. uml::

   BaseClass <|-- QuarterMaster
   QuarterMaster o- RyeMother
   

.. _tuna-infrastructure-quartermaster:   

Public Methods and Properties
-----------------------------

These are the public attributes of the `QuarterMaster`. Only `get_plugin` and `list_plugins` are meant for users, the others are building blocks.

.. autosummary::
   :toctree: api

   QuarterMaster
   QuarterMaster.list_plugins
   QuarterMaster.plugins
   QuarterMaster.get_plugin
   QuarterMaster.import_plugins

