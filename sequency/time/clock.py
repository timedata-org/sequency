from argparse import Namespace
import time

from . bar_tempo import BarTempo


"""
Variable names that end in _duration are "lengths of time" - time deltas in
seconds.

Variable names that end in _time are absolute times in seconds - like the result
of time.time().  """


class Clock(object):
    def __init__(self, tempo, get_time=time.time)
        self._tempo = tempo
        self._get_time = get_time

        self._running = False
        self._marker_time = 0
        self._marker_bars_beats = 0, 0

    @property
    def running(self):
        return self._running

    @running.setter
    def running(self, running):
        # TODO: not really thread-safe on self._running.
        if self._running == running:
            return
        self._running = running
        if running:
            self._marker_time = self._get_time()
        else:
            self._marker_bars_beats = self._tempo()

    def bars_beats(self, now=None):
        now = now or self._get_time()
        duration = now - self._marker_time
        bars, beats = self._tempo.bars_beats(duration)
        mbars, mbeats = self._marker_bars_beats

        beats += mbeats
        bars += (mbars + beats // self._tempo)
        return bars + mbars, beats + mbeats

    @property
    def bpm(self):
        return 60 / self._tempo.beat_duration

    def _mark(self):
        self._marker_time = self._get_time()
        self._marker_bars_beats = self.bars_beats(self._marker_time)

    @bpm.setter
    def bpm(self, bpm):
        # Mark the current time.
        assert bpm > 0
        self._mark()
        self.tempo.beat_duration = 60 / bpm

    @property
    def beats_per_bar(self):
        return _tempo.beats_per_bar

    @beats_per_bar.setter
    def beats_per_bar(self, beats_per_bar):
        assert beats_per_bar > 0
        self._mark()
        self.tempo.beat_duration = 60 / bpm



GLOBALS = Namespace(
    clock=clock,
    bar=lambda: clock()[0]
    bar_time=lambda: BAR_TIME,
    beat=lambda: clock()[1],
    beats_per_bar=lambda: BEATS_PER_BAR,
    now=self.timer,
    start=lambda: START,
)


@volatile
def start():
    return _START


@volatile
def now():
    return self.timer()


@volatile
def bpm():
    return BPM


@volatile
def bars():
    pass


@volatile
def beats():
    pass


@volatile
def beats():
    pass
