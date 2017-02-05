import unittest
from sequency.time.bar_tempo import BarTempo


class BarTempoTest(unittest.TestCase):
    def test_simple(self):
        bt = BarTempo()
        self.assertEqual(bt.bpm, 120)
        self.assertEqual(bt.to_beats_bars(0), (0, 0))
        self.assertEqual(bt.to_beats_bars(60), (0, 30))
        self.assertEqual(bt.to_beats_bars(61), (2.0, 30))

    def test_roundtrip(self):
        bt = BarTempo()
        for x in (-102, -7, 1, 25, 63.2, 120, 89, 999, 129319283102937812):
            self.assertAlmostEqual(x, bt.to_duration(*bt.to_beats_bars(x)))
