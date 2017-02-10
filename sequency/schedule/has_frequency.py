class HasFrequency(object):
    def __init__(self, frequency=0, period=0, on_change=None):
        if (not period) + (not frequency) != 1:
            raise ValueError('Must set exactly one of period and frequency')
        self._frequency = frequency if frequency else 1.0 / period

    @property
    def period(self):
        return 1.0 / self._frequency

    @period.setter
    def period(self, period):
        assert period > 0
        self.frequency = 1.0 / period

    @property
    def frequency(self):
        return self._frequency

    @frequency.setter
    def frequency(self, frequency):
        assert frequency > 0
        self.on_change(frequency)
        self._frequency = frequency

    def on_change(self, next_frequency):
        pass
