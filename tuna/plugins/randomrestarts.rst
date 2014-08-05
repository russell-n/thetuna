The RandomRestarts Plugin
=========================

This plugin creates the RandomRestarter optimizer.



.. uml::

   RandomRestarts --|> BasePlugin
   RandomRestarts o-- HelpPage
   RandomRestarts o-- RandomRestarter

.. _randomrestartsplugin-api:

The API
-------

.. module:: tuna.plugins.randomrestarts
.. autosummary::
   :toctree: api

   RandomRestarts
   RandomRestarts.help
   RandomRestarts.product
   RandomRestarts.sections
   RandomRestarts.fetch_config
   
