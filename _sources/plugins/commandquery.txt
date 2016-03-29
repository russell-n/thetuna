The CommandQuery Plugin
=======================

This creates a :ref:`Command Query <query-class>`.



.. uml::

   CommandQuery --|> BasePlugin
   CommandQuery o-- HelpPage
   CommandQuery o-- Query

.. _commanddump-api:

The API
-------

.. module:: tuna.plugins.commandquery
.. autosummary::
   :toctree: api

   CommandQuery
   CommandQuery.help
   CommandQuery.product
   CommandQuery.sections
   CommandQuery.fetch_config
   
