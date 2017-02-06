from . tempo import Tempo


class BarTempo(object):
    """
    Divides a tempo into equal bars.
    """
    def __init__(self, tempo=None, beats_per_bar=4):
        self.tempo = tempo or Tempo()
        self.beats_per_bar = beats_per_bar

    def to_beats_bars(self, duration):
        """
        Converts a duration in seconds to a (beats, bars) pair.
        """
        beats = duration / self.tempo.beat_duration

        total_bars = beats / self.beats_per_bar
        bars = int(total_bars)
        beats -= bars * self.beats_per_bar

        return beats, bars

    def to_duration(self, beats, bars=0):
        """
        Converts a (beats, bars) pair to a duration in seconds.
        """
        total_beats = beats + self.beats_per_bar * bars
        return total_beats * self.tempo.beat_duration
