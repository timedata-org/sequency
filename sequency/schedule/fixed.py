import time
from . import runner


def logged_sleep(self, time):
    if time > 0:
        time.sleep(time)
    elif time < 0:
        print('ERROR: ran out of time in scheduling')


class FixedScheduler(object):
    def __init__(self, clock, event, frequency, sleep=logged_sleep):
        self.runner = runner.Runner(clock, event, self.reschedule)
        self.frequency = frequency
        self.sleep = sleep

    def reschedule(self):
        self.sleep(self.delay())

    def delay(self):
        # TODO: this is wrong if we change the frequency over time!
        offset_time = (self.runner.index + 1) * self.frequency.period
        self.next_time = self.runner.start_time + offset_time
        return self.next_time - self.current_time
