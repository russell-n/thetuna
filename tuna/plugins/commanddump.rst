The CommandDump Plugin
======================

This plugin creates a :ref:`Composite <the-composite>` of :ref:`TheDump <the-dump>` command to file dumpers.



.. uml::

   CommandDump --|> BasePlugin
   CommandDump o-- HelpPage
   CommandDump o-- RandomRestarter

.. _commanddump-api:

The API
-------

.. module:: tuna.plugins.commanddump
.. autosummary::
   :toctree: api

   CommandDump
   CommandDump.help
   CommandDump.product
   CommandDump.sections
   CommandDump.fetch_config
   
