import time


class FixedFrame(object):
    def __init__(self, render, fps, sleep=time.sleep, timer=time.time,
                 report_errors=lambda x, y: None):
        self.render = render
        self.fps = fps
        self.sleep = sleep
        self.timer = timer
        self.running = True
        self.frame_count = 0
        self.report_errors = report_errors

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

    def run(self):
        self.start_time = self.timer()

        while self.running:
            self.render()

            self.next_time = self.start_time + (
                self.frame_count + 1) * self.period
            self.current_time = self.timer()
            self.delay = self.next_time - self.current_time
            if self.delay > 0:
                self.sleep(delay)
            else:
                self.report_errors(self)

            self.frame_count += 1
