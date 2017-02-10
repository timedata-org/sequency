from . import sleep


class AdaptiveLoop(sleep.SleepLoop):
    """A Loop that adjusts itself to consume some fixed portion of time.

    It estimates that the next iteration of the loop will take the arithmetic
    mean of the times it has consumed before.  You can change this strategy by
    overriding accumulate().
    """
    def __init__(self, duty_cycle=0.5, **kwds):
        """
        Args:
          duty_cycle: what portion of wall clock time should be consumed by this
              loop?
          kwds: keywords for constructor of `sleep.SleepLoop`
        """
        assert 0 < duty_cycle <= 1.0
        super().__init__(**kwds)

        self.duty_sleep = 1 / (1 - duty_cycle)
        self.accumulator = 0

    def delay(self):  # override
        mean = self.accumulate(self.after_action_time - self.before_action_time)
        return mean * self.duty_sleep

    def accumulate(self, elapsed_time):
        self.accumulator += elapsed_time
        return self.accumulator / (1 + self.count)
