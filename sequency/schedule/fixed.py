from . import scheduler


class FixedScheduler(scheduler.Scheduler):
    def __init__(self, render, fps=60, sleep=time.sleep, **kwds):
        super().__init__(render, **kwds)

        self.fps = fps
        self.sleep = sleep

    def run_frame(self):
        super.run_frame()
        self.sleep(self.delay())

    def delay(self):
        # TODO: this is wrong if we change the fps over time!
        offset = (self.frame_index + 1) * self.period
        self.next_time = self.scheduler_start + offset
        return self.next_time - self.current_time

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
