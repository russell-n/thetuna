The Stop Conditions
===================
::

    # python standard library
    import time
    
    



The Stop Conditions are callable objects used by the optimizers to decide when to stop.

Contents:

   * :ref:`The Stop Condition <optimization-components-stopcondition>`
   * :ref:`The Stop Condition with Ideal Value <optimization-components-stopcondition-ideal>`
   * :ref:`The Stop Condition Generator <optimization-components-stopcondition-generator>`

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

.. _optimization-components-stopcondition-generator:

The Stop Condition Generator
----------------------------

The StopConditionGenerator creates StopConditions (Ideal) with random end-times.

.. autosummary::
   :toctree: api

   StopConditionGenerator

::

    class StopConditionGenerator(object):
        """
        A creator of randomized stop conditions
        """
        def __init__(self, time_limit, maximum_time, minimum_time=1, 
                     end_time=None, ideal=None, delta=0, use_singleton=True, ra
    ndom_function=None):
            """
            StopConditionGenerator
    
            :param:
    
             - `time_limit`: number of seconds to generate stop-conditions
             - `maximum_time`: upper-bound on the number of seconds
             - `minimum_time`: lower-bound on the number of seconds
             - `end_time`: ctime to end
             - `ideal`: value to compare test-cases to for stop-condition
             - `delta`: amount test-case can differ from ideal
             - `use_singleton`: Generate same StopCondition object
             - `random_function`: Function to get time-out values (default is r
    andom.uniform)
            """
            self.time_limit = time_limit
            self.maximum_time = maximum_time
            self.minimum_time = minimum_time
            self.end_time = end_time
            self.ideal = ideal
            self.delta = delta
            self.use_singleton = use_singleton
            self.random_function = random_function
            self._stop_condition = None
            return
    
        @property
        def stop_condition(self):
            """
            A Stop-Condition object
            """
            #if if self._stop_condition is None or not self.use_singleton:
            #    time_limit = self.random_function(self.minimum_time, self.time
    #_limit)
            #    if self.ideal is None:
            #        self._stop_condition = StopCondition()
    
    



The StopConditionGenerator generates StopConditions. The first time it generates one it will set the end_time based on the `time_limit` unless it was already set. This way it won't exceed the maximum time. Each StopCondition will get a different time-out that's randomly generated based on the ``time_limit`` and ``minimum_time``.

.. csv-table:: StopConditionGenerator Parameters
   :header: Name, Description

   ``time_limit``, Upper-bound for the amount of time each StopCondition will run
   ``minimum_time``, Lower-bound for the amount of time each StopCondition will run
   ``end_time``, c-time to stop generation
   ``ideal``, If set the conditions will stop when the test value is close enough to it
   ``delta``, Difference from ideal for stop-condition
   ``use_singleton``, If True use same stop-condition object (but change the time-outs)
   ``random_function``, Function to use instead of random.uniform to get time-outs

Right now the times are generated uniformly, so the expected call will be ``random.uniform(minimum_time, time_limit)``. If you want to use a different function you can pass it into the constructor, so long as it can be called with the same values.

The ``use_singleton`` is a little misleading -- the ``StopConditionGenerator`` stores the object but creating a new ``StopConditionGenerator`` will create a new StopCondition so it's not a True singleton.
