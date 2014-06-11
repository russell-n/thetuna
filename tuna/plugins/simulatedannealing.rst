The SimulatedAnnealing Plugin
=============================

This plugin creates the SimulatedAnnealing optimizer.

Contents:

   * :ref:`The API <simulatedannealingplugin-api>`
   


.. uml::

   SimulatedAnnealing --|> BasePlugin
   SimulatedAnnealing o-- HelpPage
   SimulatedAnnealing o-- SimulatedAnnealer

.. _simulatedannealingplugin-api:

The API
-------

.. currentmodule:: tuna.plugins.simulatedannealing
.. autosummary::
   :toctree: api

   SimulatedAnnealing
   SimulatedAnnealing.help
   SimulatedAnnealing.product
   SimulatedAnnealing.sections
   SimulatedAnnealing.fetch_config
   
