
# this package
from optimization.optimizers.baseclimber import BaseClimber


class SteepestAscent(BaseClimber):
    """
    Steepest Ascent with Replacement
    """
    def __init__(self, local_searches, emit=False, solutions_storage=None,
                 *args, **kwargs):
        """
        Steepest Ascent Constructor

        :param:

         - `local_searches`: number of tweaks per repetition
         - `emit`: if True, print candidates as they appear
         - `solutions_storage`: object with `append` method to store solutions
        """
        super(SteepestAscent, self).__init__(*args, **kwargs)
        self.emit = emit
        self.local_searches = local_searches
        self._solutions = solutions_storage
        return

    @property
    def solutions(self):
        """
        Object to store the solutions (defaults to a list)
        """
        if self._solutions is None:
            self._solutions = []
        return self._solutions

    def __call__(self):
        """
        Runs the algorithm (sets self.solutions as side-effect)

        :return: best solution found
        """
        current = self.solution
        
        # this sets the output value for the first check
        self.quality(current)
        
        while not self.stop_condition(self.solution):
            candidate = self.tweak(current)
            
            for search in xrange(self.local_searches):
                # search around the current spot
                new_candidate = self.tweak(current)
                if self.quality(new_candidate) > self.quality(candidate):
                    candidate = new_candidate
            current = candidate
            if self.quality(current) > self.quality(self.solution):
                self.solutions.append(current)
                if self.emit:
                    print current
                self.solution = current
        return self.solution
# end SteepestAscent    


IN_PWEAVE = __name__ == '__builtin__'
#IN_PWEAVE = True


if IN_PWEAVE:
    from pweave_helpers import run_climber
    from pweave_helpers import plot_solutions
    from pweave_helpers import plot_dataset


if IN_PWEAVE:
    # python standard library
    from collections import OrderedDict
    
    # third party
    import numpy
    
    # this package
    from optimization.simulations.normalsimulation import NormalSimulation
    from optimization.components.stopcondition import StopConditionIdeal
    from optimization.components.convolutions import UniformConvolution, GaussianConvolution
    from optimization.components.xysolution import XYSolution, XYTweak        

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


if IN_PWEAVE:
    plot_solutions('normal_steepest_ascent', climber,
                   "Normal Hill Climbing Solutions (Tweak Half-range=0.1)",
                   xlabel="Solution Changes", ylabel='Solution Quality')


if IN_PWEAVE:
    plot_dataset('steepest_ascent_normal_data',
                 climber, simulator,
                 "Dataset and Solution",
                 y_offset=0.1)


if IN_PWEAVE:
    candidate.output = None
    climber._solutions = None
    climber.solution = candidate
    stop._end_time = None
    climber.local_searches = 8
    tweak.half_range = 1
    run_climber(climber)


if IN_PWEAVE:
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


if IN_PWEAVE:
    plot_solutions('needle_haystack_steepest_ascent',
                   climber,
                   "Needle In a Haystack Hill Climbing (Tweak Half-range=0.1)",
                   xlabel='Solutions', ylabel="Quality")
    print
    plot_dataset('steepest_ascent_uniform_needle_haystack_data',
                    climber, simulator,
                  "Dataset and Solution",
                  y_offset=0.1)


if IN_PWEAVE:
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


if IN_PWEAVE:
    plot_solutions('gaussian_convolution_steepest_ascent_solutions',
                   climber,
                   "Steepest Ascent with Gaussian Convolution")
    print
    plot_dataset('gaussian_convolution_steepest_ascent_dataplot',
                  climber, simulator,
                  "Dataset and Solution")


if IN_PWEAVE:
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


if IN_PWEAVE:
    plot_solutions('steepest_ascent_gaussian_convolution_normal_solutions',
                   climber,
                   "Gaussian Convolution Normal Dataset",
        xlabel='Solutions', ylabel="Quality")
    print
    plot_dataset('steepest_ascent_gaussian_convolution_normal_dataset',
                  climber, simulator,
                  "Dataset and Solution", y_offset=0.1)


if IN_PWEAVE:
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


if IN_PWEAVE:
    plot_solutions('steepest_ascent_gaussian_convolution_needle_solutions',
                   climber,
                   "Gaussian Convolution Needle Dataset",
        xlabel='Solutions', ylabel="Quality")
    print
    plot_dataset('steepest_ascent_gaussian_convolution_needle_dataset',
                  climber, simulator,
                  "Dataset and Solution", y_offset=0.1)


if IN_PWEAVE:
    for name, data in outcomes.iteritems():
        print "   {0},{1:3}".format(name, data)
