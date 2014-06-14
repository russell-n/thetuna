The Simulated Annealing Optimizer
=================================


Contents:

   * :ref:`Background <optimization-optimizers-simulatedannealing-background>`
   * :ref:`Simulated Annealing <optimization-optimizers-simulatedannealing>`
   * :ref:`Temperature Generator <optimization-optimizers-simulatedannealing-temperaturegenerator>`

.. _optimization-optimizers-simulatedannealing-background:
   
Background
----------

This optimizer uses `simulated annealing`, an nature-based approach that uses the annealing process as its model. In annealing, the rate at which a metal is allowed to cool is controlled so that the quality of the metal can be determined. If the metal is cooled rapidly it becomes hard and brittle as the molecules are pulled together tightly by the sudden drop in temperature. If the metal is cooled slowly, it becomes smoother and more pliable as the molecules are given time to arrange themselves in a uniform lattice.

The optimizer simulates annealing by starting with a high 'temperature' which causes it to explore more and then as it cools down it begins to slow its exploration. Specifically, it calculates an entropy value based on the difference between the new candidate and the previous solution and the temperature and then generates a random number which, if it is less that the entropy value, causes the learner to accept the new candidate even if it doesn't do as well as the previous solution.

.. note:: The class itself is called `SimulatedAnnealer` so that I can call the plugin `SimulatedAnnealing`

.. '

.. math::

   entropy = e^{\frac{Quality(C) - Quality(S)}{t}}\\

.. _optimization-optimizers-simulatedannealing:
   
Simulated Annealer
------------------

.. uml::

   BaseComponent <|-- SimulatedAnnealer

.. currentmodule:: tuna.optimizers.simulatedannealing
.. autosummary::
   :toctree: api

   SimulatedAnnealer
   SimulatedAnnealer.__call__
   SimulatedAnnealer.solutions



.. _optimization-optimizers-simulatedannealing-temperaturegenerator:

Temperature Generator
---------------------

.. currentmodule:: tuna.optimizers.simulatedannealing
.. autosummary::
   :toctree: api

   TemperatureGenerator
   TemperatureGenerator.__iter__

In the algorithm for simulated annealing the temperature drop is called the *temperature schedule*. In the simplest case this can be linear, although if the model is meant to be closer to nature it would need to slow its cooling as it progresses. This generator, then is meant to be a way for the user of the annealer to define how the temperature changes without having to change the annealer itself.



The TemperatureGenerator assumes that the next temperature is a function of the current temperature, which allows for linear transformations.

.. math::

   T' \gets T - \delta T\\

Or something similar. The next generator instead assumes that the transformations will be a function of the starting temperature (:math:`T_0`) and the time (number of repetitions so far). This makes it easier to do a geometric schedule like the following.

.. math::

   T(t) \gets T_0 \alpha^t\\
   
.. '

Where :math:`0 < \alpha < 1` and :math:`T_0` is the starting temperature. 

To make this work the schedule has to make use of the start time so it will be created as a method instead of a parameter. It will use the geometric progression shown above, to change it monkey patch the `schedule` method.

.. autosummary::
   :toctree: api

   TimeTemperatureGenerator
   TimeTemperatureGenerator.schedule
   TimeTemperatureGenerator.__iter__
   


Since it has an alpha value the schedule could be overridden to make a linear descent as well.

.. math::

   T \gets T_0 - \alpha t\\

Where :math:`T_0` is the start temperature (the intercept) and :math:`\alpha` is the rate of change (slope).

TimeTemperatureGenerator Builder
--------------------------------

As a starting point, I'll assume the TimeTemperatureGenerator with the default schedule is being used.

.. '

::

    # this is for clients so the strings are consistent
    class TimeTemperatureGeneratorConstants(object):
        __slots__ = ()
        # the config file needs to be wordier
        # so the option-names are longer
        # options
        start = 'start_temperature'
        stop = 'stop_temperature'
        alpha = 'alpha_temperature'
    
    



.. autosummary::
   :toctree: api

   TimeTemperatureGeneratorBuilder
   TimeTemperatureGeneratorBuilder.product

::

    class TimeTemperatureGeneratorBuilder(BaseClass):
        """
        Builds the TimeTemperatureGenerator from a dictionary
        """
        def __init__(self, configuration, section):
            """
            TimeTemperatureGeneratorBuilder constructor
            
            :param:
    
             - `configuration`: a configuration map
             - `section`: name of section with options
            """
            super(TimeTemperatureGeneratorBuilder, self).__init__()
            self.configuration = configuration
            self.section = section
            self._product = None
            return
    
        @property
        def product(self):
            """
            A built time-temperature generator
            """
            if self._product is None:
                constants = TimeTemperatureGeneratorConstants
                config = self.configuration
                try:
                    self._product = TimeTemperatureGenerator(start=config.get_f
    loat(section=self.section,
                                                                               
         option=constants.start),
                                                             stop=config.get_fl
    oat(section=self.section,
                                                                               
        option=constants.stop),
                                                             alpha=config.get_f
    loat(section=self.section,
                                                                               
         option=constants.alpha))
                except KeyError as error:
                    self.logger.error("Missing Option: {0}".format(error))
                    raise ConfigurationError("Unable to build the TimeTemperatu
    reGenerator with '{0}'".format(self.configuration))
                except ValueError as error:
                    self.logger.error(error)
                    self.log_error("Temperature values must be castable to floa
    ts")
                    raise ConfigurationError("Unable to build the TimeTemperatu
    reGenerator with '{0}'".format(self.configuration))
            return self._product
    
    

