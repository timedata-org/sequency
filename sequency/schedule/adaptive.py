from . import fixed


class AdaptiveScheduler(fixed.FixedScheduler):
    def __init__(self, render, duty_cycle=0.5, **kwds):
        super().__init__(render, **kwds)
        self.duty_cycle = duty_cycle

    def run_frame(self):
        self.start_time = self.timer()

        offset = (self.frame_index + 1) * self.period
        self.next_time = self.start_time + offset
        self.current_time = self.timer()
        self.delay = self.next_time - self.current_time
        if self.delay > 0:
            self.sleep(delay)
        else:
            self.report_errors(self)

    @property
    def period(self):
        return self._period

    @period.setter
    def period(self, period):
        self._period = period

    @property
    def fps(self):
        return 1.0 / self.period

    @fps.setter
    def fps(self, fps):
        self.period = 1.0 / fps
