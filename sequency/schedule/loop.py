import time


class Loop(object):
    """
    Repeatedly run and reschedule an action.
    """
    def __init__(self, clock, action, reschedule=None):
        """
        Args:
          clock: a clock function that returns a non-decreasing time.
          action: the action to run.
          reschedule: a function that reschedules this action. It might be
            a sleep, or nothing at all, or something else.
        """
        self.clock = clock
        self.action = action or self.action
        self.reschedule = reschedule or self.reschedule

    def run(self):
        self.count = 0
        self.start_time = self.clock()

        while self.running:
            self.run_one_action()
            self.count += 1

    def run_one_action(self):
        self.before_action = self.clock()
        self.action()

        self.after_action = self.clock()
        self.reschedule()

    def action(self):
        pass

    def reschedule(self):
        pass

    @property
    def fps(self):
        elapsed = self.clock() - self.start_time
        return self.run_count / max(1, elapsed)

    @property
    def period(self):
        elapsed = self.clock() - self.start_time
        return elapsed / max(1, self.run_count)
