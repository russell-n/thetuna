
# this package
from tuna.optimizers.baseclimber import BaseClimber


class HillClimber(BaseClimber):
    """
    A Hill-Climbing optimizer
    """
    def __init__(self, emit=True, *args, **kwargs):
        """
        HillClimber constructor

        :param:

         - `emit`: if True, print new solutions as they appear
        """
        super(HillClimber, self).__init__(*args, **kwargs)
        self.emit = emit
        self.solutions = []
        return
    
    def __call__(self):
        """
        runs the hill-climber

        :return: `best` solution found
        """
        while not self.stop_condition(self.solution):
            candidate = self.tweak(self.solution)
            if self.quality(candidate) > self.quality(self.solution):
                if self.emit:
                    print candidate
                self.solutions.append(candidate)
                self.solution = candidate
        return self.solution
# end HillClimber    


IN_PWEAVE = __name__ == '__builtin__'
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
    import datetime
    from tuna.qualities.normalsimulation import NormalSimulation
    from tuna.parts.stopcondition import StopConditionIdeal
    from tuna.tweaks.convolutions import UniformConvolution
    from tuna.parts.xysolution import XYSolution, XYTweak
    import time
    import numpy
    import matplotlib.pyplot as plt

    simulator = NormalSimulation(domain_start=-4,
                                 domain_end=4,
                                 steps=1000)

    stop = StopConditionIdeal(ideal_value=simulator.ideal_solution,
                              delta=0.0001,
                              time_limit=datetime.timedelta(seconds=300))
    
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
    
    climber = HillClimber(solution=candidate,
                          stop_condition=stop,
                          tweak=xytweak,
                          quality=simulator)
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


if IN_PWEAVE:
    plot_solutions('normal_hill_climb', climber,
                   "Normal Hill Climbing (Tweak Half-range=0.1)")    


if IN_PWEAVE:
    # make the target different so we know the data changed
    simulator.reset()
    #simulator.functions = [lambda x: 10 * x + 5]
    simulator.domain_start = -100
    simulator.domain_end = 150
    simulator.steps = 1000
    candidate.output = None
    simulator(candidate)
    climber.solution = candidate

    stop._end_time = None
    stop.ideal_value = simulator.ideal_solution

    # this takes forever, make it lenient
    tweak = UniformConvolution(half_range=1,
                               lower_bound=simulator.domain_start,
                               upper_bound=simulator.domain_end)

    xytweak = XYTweak(tweak)

    stop.delta = 0.001

    climber.tweak = xytweak
    print "Ideal: {0}".format(simulator.ideal_solution)
    run_climber(climber)


if IN_PWEAVE:
    plot_solutions('needle_haystack_hill_climb',
                   climber,
                   "Needle In a Haystack Hill Climbing (Tweak Half-range=10)")    
