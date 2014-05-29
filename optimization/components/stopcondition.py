
# python standard library
import time


class StopCondition(object):
    """
    A halting-condition for the optimizers
    """
    def __init__(self, time_limit, end_time=None):
        """
        StopCondition constructor

        :param:

         - `end_time`: (ctime) time-out
         - `time_limit`: max seconds from first call before stop
        """
        self._end_time = end_time
        self.time_limit = time_limit
        return

    @property
    def end_time(self):
        """
        C-time to stop
        """
        if self._end_time is None:
            self._end_time = self.time_limit + time.time()
        return self._end_time

    def __call__(self, solution=None):
        """
        Returns False until it's time to stop

        :param:

         - `solution`: Candidate solution, not used here
        """
        return time.time() >= self.end_time
# end StopCondition    


class StopConditionIdeal(StopCondition):
    """
    Stop condition for the optimizers with known ideal values
    """
    def __init__(self, ideal_value, delta=0.001, *args, **kwargs):
        """
        StopConditionIdeal constructor

        :param:

         - `end_time`: ctime to quit
         - `time_limit`: maximum second to allow
         - `ideal_value`: value if reached will stop the optimizers
         - `deltay`: difference from the ideal_value to accept
        """
        super(StopConditionIdeal, self).__init__(*args, **kwargs)
        self.ideal_value = ideal_value
        self.delta = delta
        
        return

    def __call__(self, solution=None):
        """
        Returns False until it's time to stop

        :param:

         - `solution`: Candidate solution to test against ideal
        """
        return (abs(solution.output - self.ideal_value) <= self.delta or
                time.time() >= self.end_time)
# end StopConditionIdeal
