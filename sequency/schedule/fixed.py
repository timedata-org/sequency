import copy
from . import sleep


class FixedLoop(sleep.SleepLoop):
    """A FixedLoop repeats with a fixed frequency, using sleep.

    The loop tries to match the absolute time each cycle, so systematic errors
    in sleep or clock arithmetic should even out over time.

    """
    def __init__(self, frequency=0, period=0, **kwds):
        super().__init__(**kwds)
        self.frequency = has_frequency.HasFrequency(
            frequency=frequency, period=period)

    def delay(self):
        loops_time = (self.loop.count + 1) * self.frequency.period
        next_time = self.loop.start_time + self.time_offset + loops_time
        return next_time - self.current_time
