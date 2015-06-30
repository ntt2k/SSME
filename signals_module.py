# Trung Nguyen

import indicators_module
import user_interface

def execute_strategies(indicator: 'indicator method', numday: int) -> [indicators_module.Stock]:
    """ generate the signals with n days """

    return indicator._signal(numday)

#########################################################################################

class SimpleMovingAverage(indicators_module.SimpleMovingAverage):

    def _signal(self, n: int) -> [indicators_module.Stock]:
        """ Generate signals strategy Simple Moving Average through out the list table """
        for i in range(len(self._new_table) - n + 1):

            if i == 0:  # skip the first number because we dont the have previous value to evaluate
                pass
            else:
                # print(i+n-1) # debug

                # If today's price is above today's moving average
                # and yesterday's price is not above yesterday's moving average
                # then BUY
                if (self._new_table[i+n-1].price > self._new_table[i+n-1].indicator) \
                        and not (self._new_table[i+n-2].price > self._new_table[i+n-2].indicator):

                    self._new_table[i+n-1] = self._new_table[i+n-1]._replace(signal = 'BUY')

                # If today's price is below today's moving average
                # and yesterday's price is not below yesterday's moving average
                # then SELL
                elif (self._new_table[i+n-1].price < self._new_table[i+n-1].indicator) \
                        and not (self._new_table[i+n-2].price < self._new_table[i+n-2].indicator):

                    self._new_table[i+n-1] = self._new_table[i+n-1]._replace(signal = 'SELL')

                else:
                    pass

        return self._new_table

#########################################################################################

class Directional(indicators_module.Directional):

    def _signal(self, n: int) -> [indicators_module.Stock]:
        """ Generate signals strategy Simple Moving Average through out the list table """
        THRESHOLD = user_interface.input_threshold()

        _temp_check_value = 'NONE'  # temporary hold value to prevent repeated print of signals
        for i in range(len(self._new_table) - n + 1):

            if (self._new_table[i+n-1].indicator > THRESHOLD[0]) and (_temp_check_value != 'BUY'):

                self._new_table[i+n-1] = self._new_table[i+n-1]._replace(signal = 'BUY')
                _temp_check_value = 'BUY'

            elif (self._new_table[i+n-1].indicator < THRESHOLD[1]) and (_temp_check_value != 'SELL'):

                self._new_table[i+n-1] = self._new_table[i+n-1]._replace(signal = 'SELL')
                _temp_check_value = 'SELL'

            else:
                pass

        return self._new_table
