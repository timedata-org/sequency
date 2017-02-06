class Tempo(object):
    """
    A tempo object that knows about bars and has an _on_change callback.
    """
    def __init__(self, beat_duration=0.5, bpm=0):
        self._beat_duration = (bpm and 60 / bpm) or beat_duration
        self.callbacks = set()

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
        self.beat_duration = 60 / bpm

    def _on_change(self, new_beat_duration):
        """
        _on_change is called just before the tempo changes, caused by setting
        beat_duration or bpm, but not beats_per_bar
        """
        for callback in self.callbacks:
            callback()
