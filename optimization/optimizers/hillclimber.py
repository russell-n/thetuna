
# this package
from optimization.optimizers.baseclimber import BaseClimber


class HillClimber(BaseClimber):
    """
    A Hill-Climbing optimizer
    """
    def __call__(self):
        """
        runs the hill-climber

        :return: `best` solution found
        """
        while not self.stop_condition(self.solution):
            candidate = self.tweak(self.solution)
            if self.quality(candidate) > self.quality(self.solution):
                print candidate.output, candidate.output - self.solution.output
                if abs(candidate.output - self.solution.output) < 0.000001:
                    import pudb; pudb.set_trace()
                    
                self.solution = candidate
        return self.solution
# end HillClimber    


def normal_hill_climb():
    simulator = NormalSimulation(domain_start=-4,
                                 domain_end=4,
                                 domain_step=0.1)

    # the stop condition does a comparison to the solutions
    # so it has to be a Solution object, not a float
    # or the Solution has to be changed to work with float comparisons
    ideal_solution = XYSolution([simulator.nearest_domain_index(simulator.ideal_solution)],
                                output=simulator.ideal_solution)
    
    stop = StopConditionIdeal(ideal_value=ideal_solution,
                              delta=0.00000001,
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
    simulator(candidate)
    
    climber = HillClimber(solution=candidate,
                          stop_condition=stop,
                          tweak=xytweak,
                          quality=simulator)
    solution = climber()
    print "solution: {0}".format(solution)
    print "Ideal: {0}".format(simulator.ideal_solution)

RUN_SIMULATION = True    
if RUN_SIMULATION:
    from optimization.simulations.normalsimulation import NormalSimulation
    from optimization.components.stopcondition import StopConditionIdeal
    from optimization.components.convolutions import UniformConvolution
    from optimization.components.xysolution import XYSolution, XYTweak
    import numpy
    normal_hill_climb()
