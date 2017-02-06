import unittest
from sequency.time.bars import BarTempo


class TempoTest(unittest.TestCase):
    def test_simple(self):
        tempo = BarTempo()
        self.assertEqual(tempo.tempo.bpm, 120)
        self.assertEqual(tempo.to_beats_bars(0), (0, 0))
        self.assertEqual(tempo.to_beats_bars(60), (0, 30))
        self.assertEqual(tempo.to_beats_bars(61), (2.0, 30))

    def test_roundtrip(self):
        tempo = BarTempo()
        for x in (-102, -7, 1, 25, 63.2, 120, 89, 999, 129319283102937812):
            beats, bars = tempo.to_beats_bars(x)
            roundtrip = tempo.to_duration(beats, bars)
            self.assertAlmostEqual(x, roundtrip)
