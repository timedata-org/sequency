class HasFrequency(object):
    DEFAULT_FREQUENCY = 60.0

    def __init__(self, frequency=0, period=0, on_change=None):
        if period:
            assert not frequency
            self.period = period
        else:
            self.frequency = frequency or DEFAULT_FREQUENCY
        self.on_change = on_change or self.on_change

    @property
    def period(self):
        return self._period

    @period.setter
    def period(self, period):
        assert period > 0
        self.on_change(period)
        self._period = period

    @property
    def frequency(self):
        return 1.0 / self.period

    @frequency.setter
    def frequency(self, frequency):
        assert frequency > 0
        self.period = 1.0 / frequency

    def on_change(self, next_period):
        pass
