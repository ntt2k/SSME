# Trung Nguyen


from collections import namedtuple

Stock = namedtuple('Stock', 'date price change indicator signal')

def Table(data: list) -> [Stock]:
    """ Generate the new namedtuple data table list to represent stock quotes """

    stocks_list = []

    for i in range(len(data) - 1):
        data_string = data[-(i+1)].split(',')
        stocks_list.append(Stock(date = data_string[0],
                                 price = float(data_string[-1]),
                                 change = 0,
                                 indicator = 0.0,
                                 signal = ''))

    return stocks_list


def run_calculations(indicator: 'indicator method', numday: int) -> [Stock]:
    """ calculating the indicator with n days """

    return indicator._calculate(numday)

#########################################################################################

class SimpleMovingAverage:

    def __init__(self, table: [Stock]):
        self._new_table = table

    def _calculate(self, n: int) -> [Stock]:
        """ Create stock lists with indicator Simple Moving Average """
        for i in range(len(self._new_table) - n + 1):
            # take a list with [n] size once at the time
            _temp_list = []
            for x in range(n):
                _temp_list.append(self._new_table[i+x].price)

            # calculate the average and input entry to the new table
            self._new_table[i+ n - 1] = self._new_table[i+ n - 1]._replace(indicator = sum(_temp_list) / n)

        return self._new_table


#########################################################################################

class Directional:

    def __init__(self, table: [Stock]):
        self._new_table = table

    def _calculate(self, n: int) -> [Stock]:
        """ Create stock lists with indicator Directional """

        for i in range(len(self._new_table)):
            # create the separate directional field column

            if i == 0:  # skip the first number because we dont the have previous value to evaluate'''
                pass

            else:

                # Calculate the direction of change every day (-1, 0, or 1)
                if self._new_table[i].price > self._new_table[i-1].price:
                    self._new_table[i] = self._new_table[i]._replace(change = 1)
                elif self._new_table[i].price < self._new_table[i-1].price:
                    self._new_table[i] = self._new_table[i]._replace(change = -1)
                else:
                    pass  # means value = 0, no need to do anything.

        for i in range(len(self._new_table) - n + 1):
            # take a list with [n] size once at the time
            _temp_list = []
            for x in range(n):
                _temp_list.append(self._new_table[i+x].change)

            # calculate the sum directional and input entry into the new table
            self._new_table[i+ n - 1] = self._new_table[i+ n - 1]._replace(indicator = sum(_temp_list))

        return self._new_table