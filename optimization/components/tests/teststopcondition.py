
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
        Does it stop if it timesout?
        """
        # does it time out?
        self.condition._end_time = random.randrange(100)
        
        self.time_mock.return_value = self.condition._end_time - 1
        with patch('time.time', self.time_mock):
            self.assertFalse(self.condition())

        self.time_mock.return_value = self.condition._end_time + 1
        with patch('time.time', self.time_mock):
            self.assertTrue(self.condition())
        return

    def test_ideal_reached(self):
        """
        Does it stop if the ideal-value is reached?
        """
        # make sure it doesn't time out
        self.time_mock.return_value = self.condition._end_time - 1
        candidate = self.condition.ideal_value - 1
        with patch('time.time', self.time_mock):
            self.assertFalse(self.condition(candidate))
            candidate = random.choice((self.condition.ideal_value,
                                       self.condition.ideal_value + 1))
            self.assertTrue(self.condition(candidate))
            
        return
