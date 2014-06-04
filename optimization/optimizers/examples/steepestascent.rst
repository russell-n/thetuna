Steepest Ascent Examples
========================


These are examples for the :ref:`Hill-Climbing with Steepest Ascent <optimization-optimizers-steepestascent>` meta-heuristic.

Contents:

   * :ref:`Normal Distribution Example <optimization-optimizers-steepestascent-normalexample>`
   * :ref:`Needle in a Haystack Example <optimization-optimizers-steepestascent-needleinahaystack>`   
   * :ref:`Gaussian Convolution Noisy Example <optimization-optimizers-steepestascent-gaussianconvolution>`
   * :ref:`Gaussian Convolution Normal Example <optimization-optimizers-steepestascent-gaussianconvolution-normal>`
   * :ref:`Gaussian Convolution Sphere Example <optimization-optimizers-steepestascent-gaussianconvolution-sphere>`

.. _optimization-optimizers-steepestascent-normalexample:

A Normal Distribution Example
-----------------------------

The SteepestAscent climber with UniformConvolution is more aggresive than the hill-climber but still has a problem with local-optima so I'll just test it on the normal-data here.

.. '

.. uml::

   HillClimber o- XYSolution
   HillClimber o- XYTweak
   HillClimber o- UniformConvolution
   HillClimber o- StopConditionIdeal
   HillClimber o- NormalSimulation

.. currentmodule:: optimization.optimizers.steepestascent
.. autosummary::
   :toctree: api

   SteepestAscent

.. currentmodule:: optimization.datamappings.normalsimulation
.. autosummary::
   :toctree: api

   NormalSimulation
.. currentmodule:: optimization.components.stopcondition 
.. autosummary::
   :toctree: api

   StopConditionIdeal
   
.. currentmodule:: optimization.components.convolutions 
.. autosummary::
   :toctree: api

   UniformConvolution
   
.. currentmodule:: optimization.components.xysolution 
.. autosummary::
   :toctree: api

   XYSolution
   XYTweak

::

    # python standard library
    from collections import OrderedDict
    
    # third party
    import numpy
    
    # this package
    from optimization.datamappings.normalsimulation import NormalSimulation
    from optimization.components.stopcondition import StopConditionIdeal
    from optimization.components.convolutions import UniformConvolution, Gaussi
    anConvolution
    from optimization.components.xysolution import XYSolution, XYTweak
    from optimization.optimizers.steepestascent import SteepestAscent
    
    

::

    outcomes = OrderedDict()
    simulator = NormalSimulation(domain_start=-4,
                                 domain_end=4,
                                 steps=1000)
    
    stop = StopConditionIdeal(ideal_value=simulator.ideal_solution,
                                  delta=0.0001,
                                  time_limit=300)
    
    tweak = UniformConvolution(half_range=0.1,
                               lower_bound=simulator.domain_start,
                               upper_bound=simulator.domain_end)
    
    xytweak = XYTweak(tweak)
    # try a bad-case to start 
    inputs = numpy.array([simulator.domain_start])
    candidate = XYSolution(inputs=inputs)
    
    climber = SteepestAscent(solution=candidate,
                             stop_condition=stop,
                             tweak=xytweak,
                             quality=simulator,
                             local_searches=4)
    outcomes['Uniform Normal'] = run_climber(climber)
    

::

    Solution: Inputs: [-0.00538732] Output: 0.398939082483
    Ideal: 0.398939082483
    Difference: 0.0
    Elapsed: 0.00937700271606
    Quality Checks: 631
    Comparisons: 315.0
    Solutions: 62
    Solutions/Comparisons: 0.196825396825
    



The number of quality checks is related to the number of comparisons made between candidate solutions::

    if Quality(solution) > Quality(candidate):
        solution = candidate

Each comparison uses two checks and there is an initializing check before the optimization starts (to establish the first candidate as the best solution found so far). So the total number of comparisons is:

.. math::

   Comparisons &\gets \frac{QualityChecks - 1}{2}\\

.. figure:: figures/normal_steepest_ascent.svg



The x-axis in the figure shows the number of times a better solution was found and the y-axis is the value (quality) of the solution. In this case the solution is a point on the x-axis and the quality is the height of the curve for the solution.


.. figure:: figures/steepest_ascent_normal_data.svg



The blue-line in the figure is a plot of the data-set while the red line is the solution found by the hill-climber.

Changing the Parameters
-----------------------

The two main parameters that will affect the performance of the climber will be the number of local searches (``SteepestAscent.local_searches``) it does and the size of the random changes it makes (``UniformConvolution.half_range``). In this case we know that the input-data is actually one-dimensional and the distribution is unimodal so it might help to reduce the number of local searches and increase the half-range to see if it will climb faster.

::

    candidate.output = None
    climber._solutions = None
    climber.solution = candidate
    stop._end_time = None
    climber.local_searches = 8
    tweak.half_range = 1
    run_climber(climber)
    
    

::

    Solution: Inputs: [-0.0021412] Output: 0.398939082483
    Ideal: 0.398939082483
    Difference: 0.0
    Elapsed: 0.00165200233459
    Quality Checks: 740
    Comparisons: 369.5
    Solutions: 6
    Solutions/Comparisons: 0.0162381596752
    
    



I tried it with different numbers of local-search values and it actually seems to take longer if you go with either fewer or more of them. I guess if there are too few then you run a greater risk of moving in the wrong-direction and if there are too many you multiply the number of searches you make before checking the overall-best solution so it inevitably uses more comparisons. I guess the parameters have to be tuned according to the data with a certain amount of trial and error.

.. _optimization-optimizers-steepestascent-needleinahaystack:

Needle In a Haystack
--------------------

Now a :ref:`Needle in a Haystack <optimization-simulations-needle-in-haystack>` case.

::

    simulator.reset()
    simulator.domain_start = -100
    simulator.domain_end = 150
    simulator.steps = 10000
    
    candidate.output = None
    climber._solutions = None
    climber.solution = candidate
    climber.emit = False
    
    stop._end_time = None
    stop.ideal_value = simulator.ideal_solution
    stop.delta = 0.001
    
    outcomes['Uniform Needle'] = run_climber(climber)
    

::

    Solution: Inputs: [-0.02358178] Output: 0.398897392943
    Ideal: 0.398922329796
    Difference: -2.49368534488e-05
    Elapsed: 0.0044629573822
    Quality Checks: 163
    Comparisons: 81.0
    Solutions: 8
    Solutions/Comparisons: 0.0987654320988
    

.. figure:: figures/needle_haystack_steepest_ascent.svg

.. figure:: figures/steepest_ascent_uniform_needle_haystack_data.svg



Since the solutions are randomly generated, the figures don't look exactly the same every time, but usually the solutions-plot for the *needle in a haystack* case will show a large dip in it as the hill-climber accidentally overshoots the peak. Since we're using *Steepest Ascent Hill Climbing* it can usually find its way back, as long as the curve has information for it and the amount of randomization is small-enough that it will eventually find the peak. In this case I'm actually cheating by using a Normal Curve, since it always has a slope leading to the peak. A true needle in the haystack case would have flat ends, but this hill climber has no real way to find that case except by chance.

.. '

.. _optimization-optimizers-steepestascent-gaussianconvolution:

Using Gaussian Convolution
--------------------------

The UniformConvolution used as the tweak tends to get stuck in local optima. You can make the half-range larger but then it will have a harder time finding an optima as it approaches randomness. One way to improve the hill-climbers is to sample random values from a normal distribution. Since 68% of the points are within one standard deviation from the mean, 95% are within two standard deviations from the mean, 99% are within three standard deviations, etc., you will tend to get most sampled points centered around the mean (0 for the standard-normal distribution) and only occasionally will you get samples that are far from the mean.

As a comparison, I'll first use a data-set that has local optima. Using the UniformConvolution doesn't always find the solution (because it's stuck at a local optima) so I'm only going to run the gaussian convolution version.

::

    # change the randomization
    tweak = GaussianConvolution(lower_bound=simulator.domain_start,
                                upper_bound=simulator.domain_end)
    tweaker = XYTweak(tweak)
    climber._solutions = None
    climber.tweak = tweaker
    
    # change the dataset
    simulator.functions = [lambda x: numpy.sin(x), 
                           lambda x: numpy.cos(x)**2]
    simulator._range = None
    simulator.quality_checks = 0
    
    candidate.output = None
    simulator(candidate)    
    climber.solution = candidate
    stop.ideal_value = simulator.ideal_solution
    stop._end_time = None
    
    # run the optimization
    outcomes['Gaussian Noise'] = run_climber(climber)
    

::

    Solution: Inputs: [ 0.44376603] Output: 1.60675092559
    Ideal: 1.60675092559
    Difference: 0.0
    Elapsed: 0.401551961899
    Quality Checks: 16130
    Comparisons: 8064.5
    Solutions: 7
    Solutions/Comparisons: 0.000868001736003
    

.. figure:: figures/gaussian_convolution_steepest_ascent_solutions.svg

.. figure:: figures/gaussian_convolution_steepest_ascent_dataplot.svg



.. _optimization-optimizers-steepestascent-gaussianconvolution-normal:

Gaussian Convolution Normal Example
-----------------------------------

To see how the two algorithms compare we can re-run the normal example using the GaussianConvolution.

::

    simulator.reset()
    simulator.domain_start = -4
    simulator.domain_end = 4
    simulator.steps = 1000
    candidate.output = None
    climber._solutions = None
    climber.solution = candidate
    stop._end_time = None
    stop.ideal_value = simulator.ideal_solution
    outcomes['Gaussian Normal'] = run_climber(climber)
    
    

::

    Solution: Inputs: [ 0.01967659] Output: 0.398862340139
    Ideal: 0.398939082483
    Difference: -7.67423442817e-05
    Elapsed: 0.00234389305115
    Quality Checks: 163
    Comparisons: 81.0
    Solutions: 5
    Solutions/Comparisons: 0.0617283950617
    
    

.. figure:: figures/steepest_ascent_gaussian_convolution_normal_solutions.svg

.. figure:: figures/steepest_ascent_gaussian_convolution_normal_dataset.svg


.. _optimization-optimizers-steepestascent-gaussianconvolution-needle:

Gaussian Convolution Needle Example
-----------------------------------

::

    simulator.reset()
    simulator.domain_start = -100
    simulator.domain_end = 150
    simulator.steps = 10000
    candidate.output = None
    climber._solutions = None
    climber.solution = candidate
    stop._end_time = None
    stop.ideal_value = simulator.ideal_solution
    outcomes['Gaussian Needle'] = run_climber(climber)
    
    

::

    Solution: Inputs: [-0.02611703] Output: 0.398897392943
    Ideal: 0.398922329796
    Difference: -2.49368534488e-05
    Elapsed: 0.00197887420654
    Quality Checks: 73
    Comparisons: 36.0
    Solutions: 3
    Solutions/Comparisons: 0.0833333333333
    
    

.. figure:: figures/steepest_ascent_gaussian_convolution_needle_solutions.svg

.. figure:: figures/steepest_ascent_gaussian_convolution_needle_dataset.svg


.. _optimization-optimizers-steepestascent-gaussianconvolution-sphere:

Gaussian Convolution Sphere
---------------------------

This uses a 3-d spherical dataset.

::

    from optimization.datamappings.examples.functions import SphereMapping
    # for plotting only we want few steps
    plot_sphere = SphereMapping(steps=120)
    
    # for data we want more
    data_sphere = SphereMapping()
    
    

::

    output = 'figures/sphere_plot.svg'
    figure = plt.figure()
    axe = figure.add_subplot(111, projection='3d')
    
    surface = axe.plot_wireframe(plot_sphere.x, plot_sphere.y, plot_sphere.z,
                                 rstride=5, cstride=5)
    figure.savefig(output)
    
    

::

    # change the data source to the sphere mapping
    simulator = data_sphere.mapping
    climber.quality = simulator
    
    # change the limits of the tweak
    tweak.lower_bound = data_sphere.start
    tweak.upper_bound = data_sphere.stop
    
    # change the candidate to 2D
    candidate.inputs = numpy.array([0,0])
    candidate.output = None
    climber._solutions = None
    climber.solution = candidate
    stop._end_time = None
    stop.ideal_value = simulator.ideal
    outcomes['Gaussian Sphere'] = run_climber(climber)
    
    

::

    Solution: Inputs: [-5.12  5.12] Output: 52.4288
    Ideal: 52.4288
    Difference: 0.0
    Elapsed: 0.00175595283508
    Quality Checks: 109
    Comparisons: 54.0
    Solutions: 6
    Solutions/Comparisons: 0.111111111111
    
    

.. figure:: figures/sphere_plot.svg




.. csv-table:: Run-Time Comparisons
   :header: ,Solutions, Comparisons, Solutions/Comparisons

   Uniform Normal,62.000,315.000,0.197
   Uniform Needle,8.000,81.000,0.099
   Gaussian Noise,7.000,8064.500,0.001
   Gaussian Normal,5.000,81.000,0.062
   Gaussian Needle,3.000,36.000,0.083
   Gaussian Sphere,6.000,54.000,0.111

