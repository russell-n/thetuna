The Base Climber
================

This is a base-class for the hill-climbing optimizers.

.. uml::

   BaseClimber <|-- HillClimber
   BaseClimber o- Tweak
   BaseClimber o- Quality
   BaseClimber o- StopCondition

.. currentmodule:: optimization.optimizers.baseclimber
.. autosummary:: 
   :toctree: api

   BaseClimber

