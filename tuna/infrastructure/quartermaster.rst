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

Auto-Generated Diagrams
-----------------------

These are auto-generated so they will always be more up-to-date than the previous class-diagrams, but they tend to be harder to read as well (and are just not pretty) so I will leave both in.

