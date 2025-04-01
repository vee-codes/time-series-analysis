import pdb

import numpy as np

MS_TO_SECONDS = 1000
SECONDS_TO_HRS = 3600


class TimeSeries:
    """The time series class is mainly made to handle 2d data where x is time,
    and y is a numerical value"""

    def __init__(self, times, values):
        dtype = [('time', 'int32'), ('value', 'int32')]
        self.data = np.array(list(zip(times, values)), dtype)

    def get_times(self):
        """Return all times"""
        return self.data['time']

    def get_values(self):
        """Return all values of the data"""
        return self.data['value']

    def get_index_at_time(self, time, match_type='gt') -> int:
        """Return the index for a particular time.
        The expectation is that all times are unique
        args:
        time: time to search for the index
        match_type: 'lt','gt','closest' used for matching if exact\
                number not found
                'lt': return exact or index one less than
                'gt': return exact or index one greater
        """
        if match_type == 'exact':
            index = np.where(self.get_times() == time)
            if len(index) > 1:
                print(
                    'WARNING: Multiple indices found for the same time,\
                            is there duplicate data in the time series')
            return index

        times = self.get_times()

        if time < times[0]:
            print(
                'Input time is less than the minimum timestamp in the data,'
                'returning the first timestamp')
            return 0
        elif time > times[-1]:
            print('Input time is greater than the max timestamp in the data,'
                  'returning the last timestamp')
            return -1

        index = np.searchsorted(times, time, 'left')
        if times[index] == time:
            return index
        if match_type == 'lt':
            return index - 1
        else:
            return index

    def get_value_at_time(self, time, match_type='gt'):
        return self.get_values()[self.get_index_at_time(time, match_type)]

    def relative_time(self, offset=0):
        self.data['time'] = self.data['time'] - self.data['time'][0]


if __name__ == "__main__":
    times = [1, 2, 3, 4, 6]
    values = [2, 4, 6, 8, 10]

    ts = TimeSeries(times, values)

    # assert ts.get_value_at_time(0) == 1
    assert ts.get_value_at_time(-1) == 2
    assert ts.get_value_at_time(0) == 2
    assert ts.get_value_at_time(5)
    assert ts.get_value_at_time(7) == 10
    assert ts.get_value_at_time(5, 'lt') == 8
