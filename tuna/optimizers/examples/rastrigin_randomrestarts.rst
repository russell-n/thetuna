Random Restarts
---------------

::

    # third-party
    import numpy
    
    # this package
    from optimization.datamappings.examples.functions import RastriginMapping
    from optimization.components.stopcondition import StopConditionGenerator
    from optimization.components.convolutions import GaussianConvolution
    from optimization.components.xysolution import XYSolutionGenerator, XYTweak
    
    from optimization.optimizers.randomrestarts import RandomRestarts
    from pweave_helpers import run_climber
    
    

::

    rastrigin_data = RastriginMapping()
    simulator = rastrigin_data.mapping
    
    stop = StopConditionGenerator(time_limit=300,
                                  maximum_time=2,
                                  minimum_time=1,
                                  ideal=simulator.ideal_solution,
                                  delta=0.0001)
    
    tweak = GaussianConvolution(lower_bound=rastrigin_data.start,
                                upper_bound=rastrigin_data.stop)
    xytweak = XYTweak(tweak)
    candidates = XYSolutionGenerator(low=rastrigin_data.start,
                                     high=rastrigin_data.stop)
    
    climber = RandomRestarts(candidates=candidates,
                             stop_conditions=stop,
                             tweak=xytweak,
                             quality=simulator)
    
    

::

    tweak.set_seed(201406041427)
    run_climber(climber)
    
    

::

    Inputs: [-4.52302417] Output: 40.3532900129
    Inputs: [-4.52301318] Output: 40.3532901198
    Inputs: [ 4.52299245] Output: 40.3532901936
    Inputs: [ 4.52299373] Output: 40.3532901938
    Solution: Inputs: [ 4.52299373] Output: 40.3532901938
    Ideal: 80.7041689429
    Difference: -40.3508787491
    Elapsed: 300.000055075
    Quality Checks: 13756050
    Comparisons: 6878024.5
    Solutions: 4
    Solutions/Comparisons: 5.81562336685e-07
    
    

