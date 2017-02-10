import time
from . import loop


class SleepLoop(loop.Loop):
    """"
    A Loop that reschedules itself by sleeping for a delay.
    """
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
            self.sleep(time)
        elif time < 0:
            print('ERROR: ran out of time in scheduling')
