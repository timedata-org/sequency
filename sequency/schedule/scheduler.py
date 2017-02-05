import time


class Scheduler(object):
    def __init__(self, render, timer=time.time):
        self.render = render
        self.timer = timer
        self._reset()

    def _reset(self):
        self.frame_index = 0
        self.scheduler_start = self.timer()

    def run(self):
        self._reset()
        while self.running:
            self.run_frame()
            self.frame_index += 1

    def run_frame(self):
        self.frame_start = self.timer()
        self.render(self.frame_start)
        self.frame_rendered = self.timer()

    @property
    def fps(self):
        return self.frame_index / max(1, self.timer() - self.scheduler_start)

    @property
    def period(self):
        return 1.0 / self.fps
