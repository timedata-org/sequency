import time


class EventLoop(object):
    """
    Repeatedly run and reschedule an event.
    """
    def __init__(self, clock, event, reschedule):
        """
        Args:
          clock: a clock function that returns a non-decreasing time.
          event: the event to run.
          reschedule: a function that reschedules this event. It might be
            a sleep, or nothing at all, or something else.
        """
        self.clock = clock
        self.event = event
        self.reschedule = reschedule

    def run(self):
        self.loop_count = 0
        self.start_time = self.clock()

        while self.running:
            self.run_one_event()
            self.loop_count += 1

    def run_one_event(self):
        self.before_event = self.clock()
        self.event()

        self.after_event = self.clock()
        self.reschedule()

    @property
    def fps(self):
        elapsed = self.clock() - self.start_time
        return self.run_count / max(1, elapsed)

    @property
    def period(self):
        elapsed = self.clock() - self.start_time
        return elapsed / max(1, self.run_count)
