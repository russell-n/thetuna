The Rastrigin Dataset
=====================

This module uses the `Rastrigin Function <http://en.wikipedia.org/wiki/Rastrigin_function>`_ to simulate data to test the optimizers.

.. currentmodule:: optimization.datamappings.examples.functions
.. autosummary:: 
   :toctree: api

   RastriginMapping

::

    # third-party
    import numpy
    from mpl_toolkits.mplot3d import Axes3D
    from matplotlib import cm
    from matplotlib.ticker import LinearLocator
    import matplotlib.pyplot as plt
    
    # this package
    from optimization.datamappings.examples.functions import RastriginMapping
    from optimization.components.stopcondition import StopConditionIdeal
    from optimization.components.convolutions import GaussianConvolution
    from optimization.components.xysolution import XYSolution, XYTweak
    from optimization.optimizers.steepestascent import SteepestAscent
    from pweave_helpers import run_climber
    
    

::

    rastrigin_data = RastriginMapping()
    rastrigin_plot = RastriginMapping(steps=200)
    simulator = rastrigin_data.mapping
    
    stop = StopConditionIdeal(ideal_value=simulator.ideal_solution,
                                       delta=0.0001,
                                       time_limit=300)
    
    tweak = GaussianConvolution(lower_bound=rastrigin_data.start,
                                upper_bound=rastrigin_data.stop)
    xytweak = XYTweak(tweak)
    candidate = XYSolution(inputs=numpy.array([0,0]))
    climber = SteepestAscent(solution=candidate,
                             stop_condition=stop,
                             tweak=xytweak,
                             quality=simulator,
                             local_searches=4)
    
    

::

    output = 'figures/rastrigin.svg'
    figure = plt.figure()
    axe = figure.add_subplot(111, projection='3d')
    surface = axe.plot_surface(rastrigin_plot.x,
                               rastrigin_plot.y,
                               rastrigin_plot.z,
                               rstride=1, cstride=1,
                               cmap=cm.coolwarm, linewidth=0, antialiased=False
    )
    axe.zaxis.set_major_locator(LinearLocator(10))
    figure.savefig(output)
    
    

.. figure:: figures/rastrigin.svg

::

    run_climber(climber)
    
    

::

    Solution: Inputs: [ 4.52327614 -4.52314047] Output: 80.706560693
    Ideal: 80.7041689429
    Difference: 0.00239175010856
    Elapsed: 300.000116825
    Quality Checks: 14025841
    Comparisons: 7012920.0
    Solutions: 19
    Solutions/Comparisons: 2.70928514798e-06
    
    

