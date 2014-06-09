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

.. '

.. math::

   entropy = e^{\frac{Quality(C) - Quality(S)}{t}}\\

.. _optimization-optimizers-simulatedannealing:
   
Simulated Annealing
-------------------

.. currentmodule:: optimization.optimizers.simulatedannealing
.. autosummary::
   :toctree: api

   SimulatedAnnealing

::

    class SimulatedAnnealing(object):
        """
        a Simulated Annealing optimizer
        """
        def __init__(self, temperatures, candidates, quality, candidate):
            """
            SimulatedAnnealing Constructor
    
            :param:
    
             - `temperatures`: a generator of temperatures
             - `candidates`: a generator of candidate solutions
             - `quality`: Quality checker for candidates
             - `candidate`: initial candidate solution
            """
            self.temperatures = temperatures
            self.candidates = candidates
            self.quality = quality
            self.solution = candidate
            return
    
        def __call__(self):
            """
            Runs the optimization
    
            :return: last non-None output given
            """
            candidates_and_temperatures = itertools.izip(self.candidates,
                                                         self.temperatures)
            solution = self.solution
            for candidate, temperature in candidates_and_temperatures:
                quality_difference = self.quality(candidate) - self.quality(sol
    ution)
                if (quality_difference > 0 or
                    random.random() < math.exp(quality_difference/float(tempera
    ture))):
                    solution = candidate
                if self.quality(solution) > self.quality(self.solution):
                    self.solution = solution
                print candidate, self.solution
            return self.solution
    # SimulatedAnnealing    
    
    



.. _optimization-optimizers-simulatedannealing-temperaturegenerator:

Temperature Generator
---------------------

.. autosummary::
   :toctree: api

   TemperatureGenerator

In the algorithm for simulated annealing the temperature drop is called the *temperature schedule*. In the simplest case this can be linear, although if the model is meant to be closer to nature it would need to slow its cooling as it progresses. This generator, then is meant to be a way for the user of the annealer to define how the temperature changes without having to change the annealer itself.
