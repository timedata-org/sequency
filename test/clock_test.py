import unittest
from sequency.time.clock import Clock


class MockTime(object):
    def __init__(self, time):
        self.time = time

    def __call__(self):
        return self.time


class ClockTest(unittest.TestCase):
    def test_simple(self):
        system_time = MockTime(0)
        clock = Clock(system_time=system_time)

        self.assertEqual(clock.bpm, 120)
        self.assertEqual(clock.time, 0)

        system_time.time += 2
        self.assertEqual(clock.time, 0)  # Not running.

        clock.running = True
        self.assertEqual(clock.time, 0)  # Running, but time hasn't advanced

        system_time.time += 1
        self.assertEqual(clock.time, 1)  # Running.

        system_time.time += 3
        self.assertEqual(clock.time, 4)  # Running.

        clock.running = False
        self.assertEqual(clock.time, 4)  # Not running.

        system_time.time += 23
        self.assertEqual(clock.time, 4)  # Not running.

        clock.running = True
        self.assertEqual(clock.time, 4)  # Not running.

        system_time.time += 5
        self.assertEqual(clock.time, 9)  # Not running.
