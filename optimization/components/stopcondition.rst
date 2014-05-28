The Stop Conditions
===================
::

    # python standard library
    import time
    
    



The Stop Conditions are callable objects used by the optimizers to decide when to stop.

Contents:

   * :ref:`The Stop Condition <optimization-components-stopcondition>`
   * :ref:`The Stop Condition with Ideal Value <optimization-components-stopcondition-ideal>`

.. _optimization-components-stopcondition:
   
The Stop Condition
------------------

.. uml::

   StopCondition : end_time
   StopCondition : time_limit
   StopCondition : __call__(solution)

.. currentmodule:: optimization.components.stopcondition
.. autosummary::
   :toctree: api

   StopCondition



.. _optimization-components-stopcondition-ideal:

Stop Condition with Ideal-Value Check
-------------------------------------

The algorithms given in [EOM]_ use two conditions for stopping -- either reaching the ideal optimization point or running out of time. I'm assuming that in most cases running out of time is the actual limit that will be used, but for the cases where a threshold is known, the StopConditionIdeal will check both the values and the time.

.. '

.. uml::

   StopCondition <|-- StopConditionIdeal

.. autosummary::
   :toctree: api

   StopConditionIdeal
   StopConditionIdeal.__call__



.. note:: the call method for the StopConditionIdeal compares the candididate solution to the ideal value using a '>=' inequality, so if solutions are objects instead of numbers they have to be able to have the inequality operations defined (e.g. ``__eq__``, ``__gte__``, etc.).
