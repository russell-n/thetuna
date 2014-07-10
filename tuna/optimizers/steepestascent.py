
# this package
from tuna.optimizers.baseclimber import BaseClimber


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

    def reset(self):
        """
        Resets some of the parameters to get ready for another trial
        """
        self._solution = None
# end SteepestAscent    
