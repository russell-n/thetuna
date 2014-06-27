
# python standard library
import unittest
import random

# third party
from mock import MagicMock

# this package
from tuna.parts.eventtimer import EventTimer
from tuna.commands.iperf.iperf import IperfClass


class TestIperf(unittest.TestCase):
    def setUp(self):
        self.dut = MagicMock()
        self.tpc = MagicMock()
        self.client_settings = MagicMock()
        self.server_settings = MagicMock()
        self.storage = MagicMock()
        self.iperf = IperfClass(dut=self.dut,
                                traffic_server=self.tpc,
                                client_settings=self.client_settings,
                                server_settings=self.server_settings,
                                storage=self.storage)
        return
    
    def test_constructor(self):
        """
        Does it build?
        """
        return

    def test_event_timer(self):
        """
        Does it build the event-timer correctly?
        """
        sleep_time = random.randrange(100)
        self.server_settings.sleep = sleep_time
        self.assertIsInstance(self.iperf.event_timer, EventTimer)
        self.assertEqual(sleep_time, self.iperf.event_timer.interval)
        return
