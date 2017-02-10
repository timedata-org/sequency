import unittest
from sequency.schedule.has_frequency import HasFrequency as Freq


class HasFrequencyTest(unittest.TestCase):
    def test_error(self):
        with self.assertRaises(ValueError):
            Freq()
        with self.assertRaises(ValueError):
            Freq(1, 1)

    def test_simple(self):
         for f in Freq(1), Freq(period=1):
            self.assertEqual(f.period, 1)
            self.assertEqual(f.frequency, 1)

    def test_exact(self):
         for f in Freq(0.5), Freq(period=2):
            self.assertEqual(f.period, 2)
            self.assertEqual(f.frequency, 0.5)

    def test_on_change(self):
        f = Freq(1)
        success = False

        f.frequency = 2
        f.period = 1
        self.assertFalse(success)

        def on_change(new_frequency):
            self.assertEqual(new_frequency, 2)
            self.assertEqual(f.frequency, 1)
            nonlocal success
            success = True

        f.on_change = on_change
        f.period = 0.5
        self.assertTrue(success)
