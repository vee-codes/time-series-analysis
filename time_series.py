import numpy as np
import pandas as pd

MS_TO_SECONDS = 1000
SECONDS_TO_HRS = 3600


class TimeSeries:
    """The time series class is mainly made to handle 2d data where x is time,
    and y is a numerical value"""

    def __init__(self, times, values):
        # initialize the empty structured array
        dtype = [('time', 'int32'), ('value', 'int32')]
        self.data = np.array(list(zip(times, values)), dtype)

    def get_times(self):
        """Return all times"""
        return self.data['time']

    def get_values(self):
        """Return all values of the data"""
        return self.data['value']

    def get_index_at_time(self, time):
        """Return the index for a particular time.
        The expectation is that all times are unique"""
        index = np.where(self.get_times() == time)[0]
        if len(index) > 1:
            print(
                'WARNING: Multiple indices found for the same time,\
                        is there duplicate data in the time series')
            return index[0]
        return index

    def get_value_at_time(self, time):
        return self.get_values()[self.get_index_at_time(time)]

    def relative_time(self, TimeSeries, offset=0):
        if not offset:
            TimeSeries[0] = TimeSeries[0] - TimeSeries[0][0]


if __name__ == "__main__":
    times = [1, 2, 3, 4]
    values = [2, 4, 6, 8]

    ts = TimeSeries(times, values)
    t = ts.get_times()

    print(t)
    print(ts.data)
    print(ts.get_value_at_time(3))
    print(ts.get_index_at_time(1))
