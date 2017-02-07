class HasFrequency(object):
    DEFAULT_FREQUENCY = 60.0

    def __init__(self, frequency=0, period=0):
        if period:
            assert not frequency
            self.period = period
        else:
            self.frequency = frequency or DEFAULT_FREQUENCY

    @property
    def period(self):
        return self._period

    @period.setter
    def period(self, period):
        assert period > 0
        self._period = period

    @property
    def frequency(self):
        return 1.0 / self.period

    @frequency.setter
    def frequency(self, frequency):
        assert frequency > 0
        self.period = 1.0 / frequency
