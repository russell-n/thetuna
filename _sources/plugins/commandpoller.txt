The CommandPoller Plugin
========================

This creates a :ref:`Command Poller <query-class>`.



.. uml::

   CommandQuery --|> BasePlugin
   CommandQuery o-- HelpPage
   CommandQuery o-- Poller

.. _commanddump-api:

The API
-------

.. module:: tuna.plugins.commandpoller
.. autosummary::
   :toctree: api

   CommandPoller
   CommandPoller.help
   CommandPoller.product
   CommandPoller.sections
   CommandPoller.fetch_config
   
