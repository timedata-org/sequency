class Tempo(object):
    """
    A tempo that also knows about bars and has a callback when it's changed.
    """
    def __init__(self, beat_duration=0.5, beats_per_bar=4, bpm=0):
        self.beats_per_bar = beats_per_bar
        self._beat_duration = (bpm and 60 / bpm) or beat_duration

    def _on_change(self, new_beat_duration):
        """This is called before self.beat_duration or self.bpm are changed,
        with the new value for beat_duration that will be set.
        """
        pass

    @property
    def beat_duration(self):
        return self._beat_duration

    @beat_duration.setter
    def beat_duration(self, beat_duration):
        assert beat_duration > 0
        self._on_change(beat_duration)
        self._beat_duration = beat_duration

    @property
    def bpm(self):
        return 60 / self._beat_duration

    @bpm.setter
    def bpm(self, bpm):
        assert bpm > 0
        self.beat_duration = 60 / bpm

    def to_beats_bars(self, duration):
        beats = duration / self._beat_duration

        total_bars = beats / self.beats_per_bar
        bars = int(total_bars)
        beats -= bars * self.beats_per_bar

        return beats, bars

    def to_duration(self, beats, bars=0):
        total_beats = beats + self.beats_per_bar * bars
        return total_beats * self._beat_duration
