
# python standard library
import unittest

# the tuna
from tuna.commands.iperf.sumparser import SumParser


test_output = """
------------------------------------------------------------
Client connecting to 192.168.103.17, TCP port 5001
TCP window size: 22.9 KByte (default)
------------------------------------------------------------
[  6] local 192.168.103.50 port 57388 connected with 192.168.103.17 port 5001
[  5] local 192.168.103.50 port 57386 connected with 192.168.103.17 port 5001
[  3] local 192.168.103.50 port 57387 connected with 192.168.103.17 port 5001
[  4] local 192.168.103.50 port 57385 connected with 192.168.103.17 port 5001
[ ID] Interval       Transfer     Bandwidth
[  6]  0.0- 1.0 sec  28.5 MBytes   239 Mbits/sec
[  5]  0.0- 1.0 sec  28.2 MBytes   237 Mbits/sec
[  3]  0.0- 1.0 sec  28.2 MBytes   237 Mbits/sec
[  4]  0.0- 1.0 sec  29.1 MBytes   244 Mbits/sec
[SUM]  0.0- 1.0 sec   114 MBytes   957 Mbits/sec
[  5]  1.0- 2.0 sec  28.0 MBytes   235 Mbits/sec
[  6]  1.0- 2.0 sec  28.1 MBytes   236 Mbits/sec
[  3]  1.0- 2.0 sec  28.0 MBytes   235 Mbits/sec
[  4]  1.0- 2.0 sec  28.0 MBytes   235 Mbits/sec
[SUM]  1.0- 2.0 sec   112 MBytes   941 Mbits/sec
[  5]  2.0- 3.0 sec  28.1 MBytes   236 Mbits/sec
[  4]  2.0- 3.0 sec  27.8 MBytes   233 Mbits/sec
[  6]  2.0- 3.0 sec  28.0 MBytes   235 Mbits/sec
[  3]  2.0- 3.0 sec  28.0 MBytes   235 Mbits/sec
[SUM]  2.0- 3.0 sec   112 MBytes   938 Mbits/sec
[  4]  3.0- 4.0 sec  27.9 MBytes   234 Mbits/sec
[  6]  3.0- 4.0 sec  27.9 MBytes   234 Mbits/sec
[  5]  3.0- 4.0 sec  28.0 MBytes   235 Mbits/sec
[  3]  3.0- 4.0 sec  27.9 MBytes   234 Mbits/sec
[SUM]  3.0- 4.0 sec   112 MBytes   936 Mbits/sec
[  3]  4.0- 5.0 sec  27.9 MBytes   234 Mbits/sec
[  4]  4.0- 5.0 sec  28.0 MBytes   235 Mbits/sec
[  6]  4.0- 5.0 sec  28.0 MBytes   235 Mbits/sec
[  5]  4.0- 5.0 sec  28.0 MBytes   235 Mbits/sec
[SUM]  4.0- 5.0 sec   112 MBytes   938 Mbits/sec
[  6]  5.0- 6.0 sec  28.0 MBytes   235 Mbits/sec
[  5]  5.0- 6.0 sec  27.9 MBytes   234 Mbits/sec
[  3]  5.0- 6.0 sec  28.0 MBytes   235 Mbits/sec
[  4]  5.0- 6.0 sec  28.1 MBytes   236 Mbits/sec
[SUM]  5.0- 6.0 sec   112 MBytes   940 Mbits/sec
[  4]  6.0- 7.0 sec  27.8 MBytes   233 Mbits/sec
[  6]  6.0- 7.0 sec  27.9 MBytes   234 Mbits/sec
[  5]  6.0- 7.0 sec  28.0 MBytes   235 Mbits/sec
[  3]  6.0- 7.0 sec  27.9 MBytes   234 Mbits/sec
[SUM]  6.0- 7.0 sec   112 MBytes   935 Mbits/sec
[  4]  7.0- 8.0 sec  28.0 MBytes   235 Mbits/sec
[  6]  7.0- 8.0 sec  28.0 MBytes   235 Mbits/sec
[  5]  7.0- 8.0 sec  27.9 MBytes   234 Mbits/sec
[  3]  7.0- 8.0 sec  28.2 MBytes   237 Mbits/sec
[SUM]  7.0- 8.0 sec   112 MBytes   941 Mbits/sec
[  4]  8.0- 9.0 sec  28.0 MBytes   235 Mbits/sec
[  6]  8.0- 9.0 sec  28.0 MBytes   235 Mbits/sec
[  5]  8.0- 9.0 sec  28.0 MBytes   235 Mbits/sec
[  3]  8.0- 9.0 sec  28.0 MBytes   235 Mbits/sec
[SUM]  8.0- 9.0 sec   112 MBytes   940 Mbits/sec
[  6]  9.0-10.0 sec  27.9 MBytes   234 Mbits/sec
[  6]  0.0-10.0 sec   280 MBytes   235 Mbits/sec
[  5]  9.0-10.0 sec  28.0 MBytes   235 Mbits/sec
[  5]  0.0-10.0 sec   280 MBytes   235 Mbits/sec
[  4]  0.0-10.0 sec   281 MBytes   236 Mbits/sec
[  3]  9.0-10.0 sec  27.9 MBytes   234 Mbits/sec
[  3]  0.0-10.0 sec   280 MBytes   235 Mbits/sec
[SUM]  0.0-10.0 sec  1.10 GBytes   940 Mbits/sec
""".split('\n')


class TestSumParser(unittest.TestCase):
    def setUp(self):
        self.parser = SumParser()
        return
    
    def test_constructor(self):
        """
        Does it build with the right defaults?
        """
        self.assertEqual(self.parser.threads,4)
        self.assertEqual(self.parser.expected_interval, 1)
        self.assertEqual(self.parser.interval_tolerance, 0.1)
        self.assertEqual(self.parser.units, 'Mbits')
        self.assertEqual(self.parser.maximum, 1000000000)
        return

    def test_test_string(self):
        """
        Does it correctly get the SUMS?
        """
        expected = [957,941,938,936,938,940,935,941,940]
        for line in test_output:
            self.parser(line)
        self.assertEqual(self.parser.intervals.values(), expected)
        return

    def test_search(self):
        """
        Does it match the SUM line?
        """
        line = '[SUM]  0.0- 1.0 sec   113 MBytes   951 Mbits/sec\n'
        match = self.parser.search(line)
        self.assertIsNotNone(match)

