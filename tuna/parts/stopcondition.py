
# python standard library
import time
import random


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
        self._time_limit = time_limit
        return

    @property
    def time_limit(self):
        """
        The max seconds to allow
        """
        return self._time_limit

    @time_limit.setter
    def time_limit(self, new_limit):
        """
        Sets the time-limit and resets the end-time

        :param:

         - `new_limit`: max seconds to allow

        :postcondition: self._end_time is None
        """
        self._time_limit = new_limit
        self._end_time = None

    @property
    def end_time(self):
        """
        C-time to stop
        """
        if self._end_time is None:
            self._end_time = self.time_limit + time.time()
        return self._end_time

    @end_time.setter
    def end_time(self, new_time):
        """
        sets the time to stop

        :param:

         - `new_time`: c-time to stop
        """
        self._end_time = new_time
        return

    def __call__(self, solution=None):
        """
        Returns False until it's time to stop

        :param:

         - `solution`: Candidate solution, not used here
        """
        return time.time() >= self.end_time

    def reset(self):
        """
        Resets the end_time to None
        """
        self._end_time = None
        return
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


class StopConditionGenerator(object):
    """
    A creator of randomized stop conditions
    """
    def __init__(self, time_limit, maximum_time, minimum_time=1, 
                 end_time=None, ideal=None, delta=0, use_singleton=True, random_function=random.uniform):
        """
        StopConditionGenerator

        :param:

         - `time_limit`: number of seconds to generate stop-conditions
         - `maximum_time`: upper-bound on the number of seconds
         - `minimum_time`: lower-bound on the number of seconds
         - `end_time`: ctime to end
         - `ideal`: value to compare test-cases to for stop-condition
         - `delta`: amount test-case can differ from ideal
         - `use_singleton`: Generate same StopCondition object
         - `random_function`: Function to get time-out values (default is random.uniform)
        """
        self.time_limit = time_limit
        self.maximum_time = maximum_time
        self.minimum_time = minimum_time
        self._end_time = end_time
        self.ideal = ideal
        self.delta = delta
        self.use_singleton = use_singleton
        self.random_function = random_function
        self._stop_condition = None
        self._global_stop_condition = None
        self.abort = False
        return

    @property
    def end_time(self):
        """
        The ctime to stop all stop-conditions (time-limit + now)
        """
        if self._end_time is None:
            self._end_time = time.time() + self.time_limit
        return self._end_time

    @property
    def global_stop_condition(self):
        """
        A stop condition using the total time instead of the random-times
        """
        if self._global_stop_condition is None:
            if self.ideal is None:
                self._global_stop_condition = StopCondition(time_limit=self.time_limit,
                                                            end_time=self.end_time)
            else:
                self._global_stop_condition = StopConditionIdeal(time_limit=self.time_limit,
                                                                 end_time=self.end_time,
                                                                 ideal_value=self.ideal,
                                                                 delta=self.delta)
        return self._global_stop_condition
    
    @property
    def stop_condition(self):
        """
        A Stop-Condition object with new end-time set every time it's retrieved
        Or a new StopCondition object every-time it's retrieved if not use_singleton
        """
        time_limit = self.random_function(self.minimum_time,
                                          self.maximum_time)
        # set an upper-bound on times
        end_time = min(time_limit + time.time(), self.end_time)

        # this probably isn't necessary, but for checks there should be
        # some consistency, I think
        if end_time == self.end_time:
            time_limit = self.time_limit

        if self._stop_condition is None or not self.use_singleton:                
            if self.ideal is None:                
                self._stop_condition = StopCondition(time_limit=time_limit,
                                                     end_time=end_time)
            else:
                self._stop_condition = StopConditionIdeal(time_limit=time_limit,
                                                          end_time=end_time,
                                                          ideal_value=self.ideal,
                                                          delta=self.delta)
        elif self.use_singleton:
            # the object existed, we need to give it new times
            self._stop_condition.time_limit = time_limit
            self._stop_condition.end_time = end_time
        return self._stop_condition

    def __iter__(self):
        """
        generates stop-conditions
        """
        while time.time() < self.end_time:
            yield self.stop_condition
            if self.abort:
                break
        return

    def reset(self):
        """
        Resets some values (assumes iter already done)
        """
        self.abort = False
        self._end_time = None
        self._global_stop_condition = None
        return