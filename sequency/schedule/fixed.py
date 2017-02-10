import copy
from . import sleep


class FixedLoop(sleep.SleepLoop):
    def __init__(self, frequency=0, period=0, **kwds):
        super().__init__(**kwds)
        self.frequency = has_frequency.HasFrequency(
            frequency=frequency, period=period)

    def delay(self):
        loops_time = (self.loop.count + 1) * self.frequency.period
        next_time = self.loop.start_time + self.time_offset + loops_time
        return next_time - self.current_time
