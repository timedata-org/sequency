class BarTempo(object):
    """
    A Tempo that also knows about bars.
    """
    def __init__(self, beat_duration=0.5, beats_per_bar=4, bpm=0)
        self.beats_per_bar = beats_per_bar
        self.beat_duration = beat_duration
        if bpm:
            self.bpm = bpm

    def bars_beats(self, duration):
        bar_duration = self.beats_per_bar * self.beat_duration
        fractional_bars = duration / bar_duration
        bars = int(fractional_bars)

        partial_bar = fractional_bars - bars
        beats = self.beats_per_bar * partial_bar

        return bars, beats

    @property
    def bpm(self):
        return 60 / self.beat_duration

    @bpm.setter
    def bpm(self, bpm):
        assert bpm > 0
        self.beat_duration = 60 / bpm

    def add(self, bars_beats1, bars_beats2):
        pass
