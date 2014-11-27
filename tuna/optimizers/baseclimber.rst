The Base Climber
================

This is a base-class for the hill-climbing optimizers.

.. uml::

   BaseClimber <|-- HillClimber
   BaseClimber o- Tweak
   BaseClimber o- Quality
   BaseClimber o- StopCondition

.. currentmodule:: tuna.optimizers.baseclimber
.. autosummary:: 
   :toctree: api

   BaseClimber



Right now only the constructor is defined. I'm not sure how much use it is.
