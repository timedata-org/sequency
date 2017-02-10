from . import sleep


class AdaptiveLoop(sleep.SleepLoop):
    def __init__(self, duty_cycle=0.5, **kwds):
        assert 0 < duty_cycle <= 1.0
        super().__init__(**kwds)
        self.duty_cycle = duty_cycle
        self.duty_sleep = 1 / duty_cycle - 1
        self.accumulator = 0

    def delay(self):
        self.accumulate(self.after_action_time - self.before_action_time)
        return self.mean() * self.duty_sleep

    def accumulate(self, elapsed_time):
        self.accumulator += elapsed_time

    def mean(self):
        return self.accumulator / max(1, self.count)
