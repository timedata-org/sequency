from . import Loop

import time


class SleepLoop(object):
    def __init__(self, clock, action, sleep=None, delay=None):
        super().__init__(clock, action)
        self.sleep = sleep or self.sleep
        self.delay = delay or self.delay

    def reschedule(self):
        self.sleep(self.delay())

    def delay(self):
        return 0

    def sleep(self, time):
        if time > 0:
            time.sleep(time)
        elif time < 0:
            print('ERROR: ran out of time in scheduling')


class FixedScheduler(object):
    def __init__(self, frequency):
        self.frequency = frequency
        self.sleep = sleep

        frequency.on_change = self.on_change

    def on_change(self, next_period):
        delta = next_period - self.frequency.period
        self.time_offset +=

    def loop_time(self):
        return (self.loop.count + 1) * self.frequency.period

    def delay(self):
        next_time = self.loop.start_time + self.time_offset + self.loop_time()
        return next_time - self.current_time
