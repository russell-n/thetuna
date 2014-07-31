The GridSearch Plugin
=====================   

This plugin creates the ExhaustiveSearch optimizer.



.. uml::

   GridSearch --|> BasePlugin
   GridSearch o-- HelpPage
   GridSearch o-- ExhaustiveSearch

.. _gridsearchplugin-api:

The API
-------

.. currentmodule:: tuna.plugins.gridsearch
.. autosummary::
   :toctree: api

   GridSearch
   GridSearch.help
   GridSearch.product
   GridSearch.sections
   GridSearch.fetch_config
   
