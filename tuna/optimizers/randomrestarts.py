
# python standard library
import datetime

# This package
from tuna.components.component import BaseComponent
from tuna import LOG_TIMESTAMP


class RandomRestarter(BaseComponent):
    """
    Hill-climbing with random restarts
    """
    def __init__(self, local_stops, quality, tweak,
                 solution_storage,
                 candidate=None, 
                 global_stop=None, observers=None):
        """
        Random Restarts constructor

        :param:

         - `local_stops`: generator of stop-conditions with random time-outs
         - `quality`: callable that assesses candidate solutions
         - `tweak`: callable to tweak existing candidate solutions         
         - `solution_storage`: object to write solutions to
         - `candidate` : initial candidate (takes from global_stop parameter if not given)
         - `global_stop`: callable to decide to stop (takes from local_stops if not given)
         - `observers`: Composite of objects to give final solution to
        """
        super(RandomRestarter, self).__init__()
        self.tabu = set([])
        self.local_stops = local_stops
        self.tweak = tweak
        self.quality = quality
        self._candidate = None
        self.candidate = candidate
        self._solution = candidate
        self.solutions = solution_storage
        self._global_stop = global_stop
        self.observers = observers
        return

    @property
    def candidate(self):
        """
        initial candidate solution (does quality check first time used)
        """
        if self._candidate is None:
            self._candidate = self.tabu_search()
        elif str(self._candidate.output) is None:
            self.quality(self._candidate)
        return self._candidate

    @candidate.setter
    def candidate(self, new_candidate):
        """
        Sets the candidate, adds to tabu-set

        :param:

         - `new_candidate`: candidate solution
        """
        self._candidate = new_candidate
        if new_candidate is not None:
            self.tabu.add(str(new_candidate.inputs))
        return

    @property
    def solution(self):
        """
        Best Candidate solution so far
        """
        if self._solution is None:
            self._solution = self.candidate
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
    def global_stop(self):
        """
        StopCondition to stop all testing
        """
        if self._global_stop is None:
            self._global_stop = self.local_stops.global_stop_condition
        return self._global_stop

    def __call__(self):
        """
        Finds the best solution within given time
        """
        self.reset()
        candidate = self.solution
        self.log_info("Initial Best Solution: {0}".format(candidate))
        # start the data log
        self.solutions.write("Time,Checks,Solution\n")       
        timestamp = datetime.datetime.now().strftime(LOG_TIMESTAMP)
        output = "{0},1,{1}\n".format(timestamp, candidate)
        self.solutions.write(output)
        self.logger.info("First Candidate: {0}".format(candidate))
        
        for local_stop in self.local_stops:
            # global search
            if self.global_stop(self.solution):
                self.log_info(('Stop condition reached '
                               'with solution: {0}').format(self.solution))
                break

            while not local_stop(candidate):
                # local-search
                new_candidate = self.tabu_search(candidate)
                
                self.logger.debug("Trying candidate: {0}".format(new_candidate))
                if self.quality(new_candidate) > self.quality(candidate):
                    candidate = new_candidate
                    self.logger.info("Candidate '{0}' new local solution".format(candidate))
                    
            if self.quality(candidate) > self.quality(self.solution):
                timestamp = datetime.datetime.now().strftime(LOG_TIMESTAMP)
                output = "{0},{1},{2}\n".format(timestamp,
                                                self.quality.quality_checks,
                                                candidate)
                self.solutions.write(output)
                self.log_info("New Best Solution: {0}".format(output))                
                self.solution = candidate

            # random restart
            self.log_info("Random Restart")
            candidate = self.tabu_search()
            self.logger.debug("Trying candidate: {0}".format(candidate))

        self.log_info("Quality Checks: {0} Solution: {1} ".format(self.quality.quality_checks,
                                                                     self.solution))
        if self.observers is not None:
            # this is for users of the solution
            self.log_info("RandomRestarter giving solution to '{0}'".format(self.observers))
            self.observers(target=self.solution)
        return self.solution

    def tabu_search(self, candidate=None):
        """
        Tweaks the candidate until it finds a new one

        :param:

         - `candidate`: candidate solution to tweak (None to get random candidate)

        :postcondition: string of new candidate.input in tabu set
        :return: new candidate
        """
        self.logger.debug(("Searching for a local "
                                   "candidate not in the tabu space"))
        new_candidate = self.tweak(candidate)
        while (str(new_candidate.inputs) in self.tabu and
                       not self.global_stop(self.solution)):
                new_candidate = self.tweak(candidate)
        self.tabu.add(str(new_candidate.inputs))

        # set the quality so the stop-conditions will work
        self.quality(new_candidate)
        return new_candidate        

    def check_rep(self):
        """
        no-op for now
        """
        return

    def close(self):
        """
        Closes solutions, quality
        """
        self.solutions.close()
        self.quality.close()
        self._solution = None
        return

    def reset(self):
        """
        Clears and resets the parts
        """
        self.logger.debug("Resetting the RandomRestarter parts")
        self.tabu.clear()
        self.quality.reset()
        self.local_stops.reset()
        self._solution = None
        self.solutions.reset()
        self.global_stop.reset()
        return

# end RandomRestarter        
