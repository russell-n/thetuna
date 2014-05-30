Hill-Climbing with Random Restarts
==================================


*Hill-Climbing With Random Restarts* generalizes hill-climbing to make a global classifier _[EOM]. It does this by periodically restarting in a new spot. To enable the restarting, an inner-loop is created that runs for the amount of time (repetitions?) chosen from a distribution of times. Once the time for the inner loop is finished a new candidate is randomly generated and process restarts until the total time expires or the ideal solution is found (in the theoretical case).

.. currentmodule:: optimization.optimizers.randomrestarts
.. autosummary::
   :toctree: api

   RandomRestarts
   RandomRestarts.__call__
   RandomRestarts.solution
   RandomRestarts.solutions
   RandomRestarts.is_ideal



Example Use
-----------

First we'll start with the normal distribution. 

.. '

::

    IN_PWEAVE = __name__ == '__builtin__'
    if IN_PWEAVE:
        # helpers for weaving
        from pweave_helpers import run_climber, plot_dataset    
    
        # actual builder code
        from optimization.components.convolutions import UniformConvolution
        from optimization.simulations.normalsimulation import NormalSimulation
        from optimization.components.xysolution import XYSolutionGenerator, XYTweak
        from optimization.components.stopcondition import StopConditionGenerator
    
        simulator = NormalSimulation(domain_start=-4,
                                     domain_end=4,
                                     domain_step=0.1)
    
        stop_conditions = StopConditionGenerator(time_limit=300,
                                                 maximum_time=0,
                                                 minimum_time=0,
                                                 ideal=simulator.ideal_solution,
                                                 delta=0.000000001)
        tweak = UniformConvolution(half_range=0.1,
                                   lower_bound=simulator.domain_start,
                                   upper_bound=simulator.domain_end)
        xy_tweak = XYTweak(tweak)
        candidates = XYSolutionGenerator(low=simulator.domain.min(),
                                         high=simulator.domain.max())
        
        climber = RandomRestarts(stop_conditions=stop_conditions,
                                 candidates=candidates,
                                 quality=simulator,
                                 tweak=xy_tweak)
    
        run_climber(climber, simulator)    
    

::

    Inputs: [ 0.00181747] Output: 0.398942280401
    solution: Inputs: [ 0.00181747] Output: 0.398942280401
    Ideal: 0.398942280401
    Difference: 0.0
    Elapsed: 0.000504016876221
    

.. figure:: figures/random_restart_normal.svg

