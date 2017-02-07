import time


class Runner(object):
    def __init__(self, clock, event, reschedule):
        self.clock = clock
        self.event = event
        self.reschedule = reschedule

    def run(self):
        self.cycles = 0
        self.start_time = self.clock()

        while self.running:
            self.before_event = self.clock()
            self.event()

            self.after_event = self.clock()
            self.reschedule()

            self.cycles += 1

    @property
    def fps(self):
        return self.cycles / max(1, self.clock() - self.start_time)

    @property
    def period(self):
        return 1.0 / self.fps
