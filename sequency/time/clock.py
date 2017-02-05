from argparse import Namespace
import copy, time

from . tempo import Tempo


class Clock(Tempo):
    def __init__(self, system_time=time.time, **kwds):
        super().__init__(**kwds)

        self.system_time = system_time
        self._running = False
        self._time = 0

    @property
    def time(self):
        if self.running:
            return self.system_time() - self._time
        return self._time

    @time.setter
    def time(self, time):
        if self._running:
            self._time = self.system_time() - time
        else:
            self._time = time

    @property
    def running(self):
        return self._running

    @running.setter
    def running(self, running):
        # TODO: not really thread-safe on self._running.
        if self._running != running:
            if running:
                self._time = self.system_time() - self._time
            else:
                self._time = self.time
            self._running = running

    def _on_change(self, new_beat_duration):
        self.time *= new_beat_duration / self.tempo.beat_duration
