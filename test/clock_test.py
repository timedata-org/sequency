import unittest
from sequency.time.clock import Clock


class MockTime(object):
    def __init__(self, time):
        self.time = time

    def __call__(self):
        return self.time


class ClockTest(unittest.TestCase):
    def test_story(self):
        system_time = MockTime(0)
        clock = Clock(system_time=system_time)

        self.assertEqual(clock.bpm, 120)
        self.assertEqual(clock(), 0)

        system_time.time += 2
        self.assertEqual(clock.time, 0)  # Not running.
        self.assertEqual(clock(), clock.time)

        clock.running = True
        self.assertEqual(clock.time, 0)  # Running, but time hasn't advanced

        # Do it again.
        clock.running = True
        self.assertEqual(clock.time, 0)

        system_time.time += 1
        self.assertEqual(clock.time, 1)

        system_time.time += 3
        self.assertEqual(clock.time, 4)

        clock.running = False
        self.assertEqual(clock.time, 4)

        system_time.time += 23
        self.assertEqual(clock.time, 4)

        clock.running = True
        self.assertEqual(clock.time, 4)

        system_time.time += 5
        self.assertEqual(clock.time, 9)

        # Try setting the time when it's running, and not running.
        clock.time = 12
        self.assertEqual(clock.time, 12)

        system_time.time += 7
        self.assertEqual(clock.time, 19)

        clock.running = False
        self.assertEqual(clock.time, 19)

        system_time.time += 100
        clock.time = 23
        self.assertEqual(clock.time, 23)

        system_time.time += 100
        clock.running = True
        system_time.time += 1
        self.assertEqual(clock.time, 24)

    def test_on_change(self):
        system_time = MockTime(0)
        clock = Clock(system_time=system_time)
        self.assertEqual(clock.bpm, 120)
        clock.running = True

        system_time.time += 10
        self.assertEqual(clock.time, 10)
        clock.bpm = 60
        self.assertEqual(clock.time, 20)
