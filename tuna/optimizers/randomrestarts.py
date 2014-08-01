
# python standard library
import itertools


class RandomRestarts(object):
    """
    Hill-climbing with random restarts
    """
    def __init__(self, stop_conditions, candidates, quality, tweak, solution=None,
                 solution_storage=None, is_ideal=None, emit=True):
        """
        Random Restarts constructor

        :param:

         - `stop_conditions`: generator of stop-conditions with random time-outs
         - `candidates`: generator of candidate solutions
         - `quality`: callable that assesses candidate solutions
         - `tweak`: callable to tweak existing candidate solutions         
         - `solution_storage`: object to append solutions to
         - `solution` : initial candidate (takes from candidates parameter if not given)
         - `is_ideal`: callable to assess if solution is ideal
         - `emit`: if true, print new solutions
        """
        self._solutions = solution_storage
        self.stop_conditions = stop_conditions
        self.candidates = candidates
        self.quality = quality
        self.tweak = tweak
        self._is_ideal = is_ideal
        self._solution = solution
        self.emit = emit
        return

    @property
    def solutions(self):
        """
        collection to store all solutions (default: list)
        """
        if self._solutions is None:
            self._solutions = []
        return self._solutions

    @property
    def solution(self):
        """
        Best Candidate solution so far
        """
        if self._solution is None:
            self._solution = self.candidates.candidate
        return self._solution

    @solution.setter
    def solution(self, new_solution):
        """
        Sets the solution

        :param:

         - `new_solution`: Best solution so far
        """
        self._solution = new_solution
        return

    @property
    def is_ideal(self):
        """
        StopCondition to stop all testing
        """
        if self._is_ideal is None:
            self._is_ideal = self.stop_conditions.global_stop_condition
        return self._is_ideal

    def __call__(self):
        """
        Finds the best solution within given time
        """
        candidates_stop_locals = itertools.izip(self.candidates, self.stop_conditions)
        for candidate, local_stop in candidates_stop_locals:
            self.quality(candidate)
            while not local_stop(candidate):
                new_candidate = self.tweak(candidate)
                if self.quality(new_candidate) > self.quality(candidate):
                    candidate = new_candidate
            if self.quality(candidate) > self.quality(self.solution):
                self.solutions.append(candidate)
                self.solution = candidate
                if self.emit:
                    print candidate
            # this is needed to check if the solution is ideal
            if self.is_ideal(self.solution):
                break
        return self.solution

    def reset(self):
        """
        Resets solutions (this only works if it is a list)
        """
        self._solutions = None
        return        
# end RandomRestarts        


IN_PWEAVE = __name__ == '__builtin__'
if IN_PWEAVE:
    # python standard library
    import datetime
    
    # helpers for weaving
    from examples.pweave_helpers import run_climber, plot_dataset    

    # actual builder code
    from tuna.tweaks.convolutions import UniformConvolution
    from tuna.qualities.normalsimulation import NormalSimulation
    from tuna.parts.xysolution import XYSolutionGenerator, XYTweak
    from tuna.parts.stopcondition import StopConditionGenerator

    simulator = NormalSimulation(domain_start=-4,
                                 domain_end=4,
                                 steps=1000)

    stop_conditions = StopConditionGenerator(time_limit=datetime.timedelta(seconds=300),
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

    run_climber(climber)    


if IN_PWEAVE:
    plot_dataset("random_restart_normal", climber, simulator,
                 "Random Restarts Normal Dataset")
