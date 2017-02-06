import time


class Scheduler(object):
    def __init__(self, event, clock):
        self.event = event
        self.clock = clock
        self._reset()

    def _reset(self):
        self.index = 0
        self.scheduler_start = self.clock()

    def run_loop(self):
        self._reset()
        while self.running:
            self.run()
            self.index += 1

    def run(self):
        self.before_event = self.clock()
        self.event()
        self.after_event = self.clock()

    @property
    def fps(self):
        return self.index / max(1, self.clock() - self.scheduler_start)

    @property
    def period(self):
        return 1.0 / self.fps
