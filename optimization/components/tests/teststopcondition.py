
# python standard library
import unittest
import random

# third-party
from mock import MagicMock, patch

# this package
from optimization.components.stopcondition import StopCondition, StopConditionIdeal


class TestStopCondition(unittest.TestCase):
    def setUp(self):
        self.time_mock = MagicMock(name='time')
        self.end_time = random.randrange(100)
        self.time_limit = random.randrange(100)
        self.condition = StopCondition(end_time=self.end_time,
                                       time_limit=self.time_limit)
        return
        
    def test_constructor(self):
        """
        Does it build?
        """
        self.assertEqual(self.time_limit, self.condition.time_limit)
        self.assertEqual(self.condition.end_time, self.end_time)
        return

    def test_end_time(self):
        """
        Does it set the end-time?
        """
        current_time = random.randrange(100)
        self.time_mock.return_value = current_time
        self.condition._end_time = None
        with patch('time.time', self.time_mock):
            self.assertEqual(self.time_limit + current_time,
                             self.condition.end_time)
        return

    def test_call(self):
        """
        Does it stop when it's out of time?
        """
        # is it callable?
        solution = random.randrange(10)
        self.condition(solution)

        # does it time out?
        self.condition._end_time = random.randrange(100)
        
        self.time_mock.return_value = self.condition._end_time - 1
        with patch('time.time', self.time_mock):
            self.assertFalse(self.condition())

        self.time_mock.return_value = self.condition._end_time + 1
        with patch('time.time', self.time_mock):
            self.assertTrue(self.condition())
        return    


class TestStopConditionIdeal(unittest.TestCase):
    def setUp(self):
        self.time_mock = MagicMock(name='time')
        self.end_time = random.randrange(100)
        self.time_limit = random.randrange(100)
        self.ideal_value = random.randrange(100)
        self.condition = StopConditionIdeal(end_time=self.end_time,
                                       time_limit=self.time_limit,
            ideal_value=self.ideal_value)

        return
    
    def test_constructor(self):
        """
        Does it build?
        """
        self.assertIsInstance(self.condition, StopCondition)
        return

    def test_timeout(self):
        """
        Does it stop if it times-out?
        """
        # does it time out?
        self.condition._end_time = random.randrange(100)
        
        self.time_mock.return_value = self.condition._end_time - 1

        # make sure it doesn't reach a good solution
        solution = MagicMock()
        solution.output = self.condition.ideal_value + 2
        solution.delta = 0
        with patch('time.time', self.time_mock):
            self.assertFalse(self.condition(solution))

        self.time_mock.return_value = self.condition._end_time + 1
        with patch('time.time', self.time_mock):
            self.assertTrue(self.condition(solution))
        return

    def test_ideal_reached(self):
        """
        Does it stop if the ideal-value is reached?
        """
        # make sure it doesn't time out
        self.condition.delta = 0.1
        self.time_mock.return_value = self.condition._end_time - 1
        candidate = MagicMock()
        candidate.output = self.condition.ideal_value - 1
        
        with patch('time.time', self.time_mock):
            msg = "Candidate: {0}, Ideal: {1}".format(candidate.output,
                                                      self.condition.ideal_value)
            self.assertFalse(self.condition(candidate),
                             msg=msg)

            self.condition.delta = 10
            candidate.output = random.choice((self.condition.ideal_value,
                                       self.condition.ideal_value + 1))
            msg = "Candidate: {0}, Ideal: {1}".format(candidate.output,
                                                      self.condition.ideal_value)

            self.assertTrue(self.condition(candidate), msg=msg)            
        return
