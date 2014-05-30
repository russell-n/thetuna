
# this package
from optimization.optimizers.baseclimber import BaseClimber


class SteepestAscent(BaseClimber):
    """
    Steepest Ascent with Replacement
    """
    def __init__(self, local_searches, emit=True, *args, **kwargs):
        """
        Steepest Ascent Constructor

        :param:

         - `local_searches`: number of tweaks per repetition
         - `emit`: if True, print candidates as they appear
        """
        super(SteepestAscent, self).__init__(*args, **kwargs)
        self.emit = emit
        self.local_searches = local_searches
        self.solutions = []
        return

    def __call__(self):
        """
        Runs the algorithm (sets self.solutions as side-effect)

        :return: best solution found
        """
        current = self.solution
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
def run_climber(climber):
    start = time.time()
    solution = climber()
    end = time.time()
    print "solution: {0}".format(solution)
    print "Ideal: {0}".format(simulator.ideal_solution)
    print "Difference: {0}".format(solution.output - simulator.ideal_solution)
    print "Elapsed: {0}".format(end - start)
    return

if IN_PWEAVE:
    from optimization.simulations.normalsimulation import NormalSimulation
    from optimization.components.stopcondition import StopConditionIdeal
    from optimization.components.convolutions import UniformConvolution, GaussianConvolution
    from optimization.components.xysolution import XYSolution, XYTweak
    import time
    import numpy
    import matplotlib.pyplot as plt

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
    inputs = numpy.random.uniform(simulator.domain_start,
                                  simulator.domain_end,
                                  size=1)
    candidate = XYSolution(inputs=inputs)

    # this is a kludge until I get the call-ordering worked out
    # right now the simulator is setting the .output as a side-effect
    simulator(candidate)
    
    climber = SteepestAscent(solution=candidate,
                             stop_condition=stop,
                             tweak=xytweak,
                             quality=simulator,
                             local_searches=4)
    run_climber(climber)

def plot_solutions(filename, climber, title):
    output = 'figures/{0}.svg'.format(filename)
    figure = plt.figure()
    axe = figure.gca()
    data = [solution.output for solution in climber.solutions]
    axe.plot(data)
    axe.set_title(title)
    figure.savefig(output)
    print '.. figure:: '  + output
    return

def plot_dataset(filename, climber, simulator, title):
    output = 'figures/{0}.svg'.format(filename)
    figure = plt.figure()
    axe = figure.gca()
    axe.plot(simulator.domain, simulator.range)
    axe.axhline(climber.solution.output, color='r')
    figure.savefig(output)
    print ".. figure:: " + output
    return


if IN_PWEAVE:
    plot_solutions('normal_steepest_ascent', climber,
                   "Normal Hill Climbing (Tweak Half-range=0.1)")


#import pudb; pudb.set_trace()
if IN_PWEAVE:
    plot_dataset('steepest_ascent_normal_data',
                 climber, simulator,
                 "Dataset and Solution")


if IN_PWEAVE:
    # make the target different so we know the data changed
    simulator.reset()
    #simulator.functions = [lambda x: 10 * x + 5]
    simulator.domain_start = -100
    simulator.domain_end = 150
    simulator.domain_step = 0.1
    candidate.output = None
    simulator(candidate)
    climber.solution = candidate
    climber.emit = False

    stop._end_time = None
    stop.ideal_value = simulator.ideal_solution

    tweak = UniformConvolution(half_range=0.1,
                               lower_bound=simulator.domain_start,
                               upper_bound=simulator.domain_end)

    xytweak = XYTweak(tweak)

    stop.delta = 0.001

    climber.tweak = xytweak
    print "Ideal: {0}".format(simulator.ideal_solution)
    run_climber(climber)


if IN_PWEAVE:
    plot_solutions('needle_haystack_steepest_ascent',
                   climber,
                   "Needle In a Haystack Hill Climbing (Tweak Half-range=0.1)")
    print
    plot_dataset('steepest_ascent_needle_haystack_data',
                  climber, simulator,
                  "Dataset and Solution")


if IN_PWEAVE:
    # change the randomization
    tweak = GaussianConvolution(lower_bound=simulator.domain_start,
                                upper_bound=simulator.domain_end)
    tweaker = XYTweak(tweak)
    climber.tweak = tweaker

    # change the dataset
    simulator.functions = [lambda x: numpy.sin(x), 
                           lambda x: numpy.cos(x)**2]
    simulator._range = None
    candidate.output = None
    simulator(candidate)    
    climber.solution = candidate
    stop.ideal_value = simulator.ideal_solution
    stop._end_time = None

    # run the optimization
    run_climber(climber)


if IN_PWEAVE:
    plot_solutions('gaussian_convolution_steepest_ascent_solutions',
                   climber,
                   "Steepest Ascent with Gaussian Convolution")
    print
    plot_dataset('gaussian_convolution_steepest_ascent_dataplot',
                  climber, simulator,
                  "Dataset and Solution")
