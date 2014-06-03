The BaseSimulation
==================

This is a base-class for data-simulation classes.



Dependencies
------------

.. currentmodule:: numpy
.. autosummary::
   :toctree: api

   arange
   abs
   argmin

The BaseSimulation Class
------------------------

.. uml::

   BaseSimulation : domain
   BaseSimulation : domain_start
   BaseSimulation : domain_end
   BaseSimulation : domain_step

.. currentmodule:: optimization.simulations.basesimulation
.. autosummary::
   :toctree: api

   BaseSimulation
   BaseSimulation.domain
   BaseSimulation.nearest_domain_index
   BaseSimulation.__call__

