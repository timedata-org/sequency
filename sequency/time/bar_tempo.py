class BarTempo(object):
    """
    A Tempo that also knows about bars.
    """
    def __init__(self, beat_duration=0.5, beats_per_bar=4, bpm=0):
        self.beats_per_bar = beats_per_bar
        self.beat_duration = beat_duration
        self.bpm = bpm or self.bpm

    @property
    def bpm(self):
        return 60 / self.beat_duration

    @bpm.setter
    def bpm(self, bpm):
        assert bpm > 0
        self.beat_duration = 60 / bpm
        self.bar_duration = self.beats_per_bar * self.beat_duration

    def to_beats_bars(self, duration):
        beats = duration / self.beat_duration

        total_bars = beats / self.beats_per_bar
        bars = int(total_bars)
        beats -= bars * self.beats_per_bar

        return beats, bars

    def to_duration(self, beats, bars=0):
        total_beats = beats + self.beats_per_bar * bars
        return total_beats * self.beat_duration
