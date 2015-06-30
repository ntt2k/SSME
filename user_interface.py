# Trung Nguyen

import download_module
import indicators_module
import signals_module

def _input_symbol() -> str:
    """ Input company code symbol """
    print('Please input a company symbol to analysis (press Enter or Return to quit)')
    symbol = input('SYMBOL: ').strip().upper()

    if symbol == '':
        return ''
    else:
        return symbol


def _input_date_range(symbol: str) -> str:
    """ Take 1 parameter str 'symbol' code and input date range from user to produce url """

    while True:
        try:
            SYMBOL = symbol

            from datetime import datetime
            START_DATE = datetime.strptime(input('START DATE: ').strip(), '%Y-%m-%d').date()

            if START_DATE <= datetime.now().date():

                END_DATE = datetime.strptime(input('END DATE: ').strip(), '%Y-%m-%d').date()
                if (END_DATE <= datetime.now().date()) and (END_DATE > START_DATE):

                    START_MONTH = str(int(START_DATE.strftime('%m')) - 1)
                    START_DAY = START_DATE.strftime('%d')
                    START_YEAR = START_DATE.strftime('%Y')
                    END_MONTH = str(int(END_DATE.strftime('%m')) - 1)
                    END_DAY = END_DATE.strftime('%d')
                    END_YEAR = END_DATE.strftime('%Y')

                    return 'http://ichart.yahoo.com/table.csv?s='\
                           + SYMBOL + '&a='\
                           + START_MONTH + '&b='\
                           + START_DAY + '&c='\
                           + START_YEAR + '&d='\
                           + END_MONTH + '&e='\
                           + END_DAY + '&f='\
                           + END_YEAR + '&g=d'
                else:
                    print('The end date should be on or before today\'s date, \
                    and should also be later than the start date.\nPlease try again ...\n')
            else:
                print('The start date should be on or before today\'s date\'. Please try again ...\n')
        except ValueError:
            print('The date is entered in an incorrect format (YYYY-MM-DD). Please try again ...\n')


def _input_indicator() -> str:
    """ Input indicator method """
    while True:
        idt = input('Please choose indicator Simple Moving Average (sma) or Directional (direct): ').strip()

        if idt == 'sma':
            return 'SimpleMovingAverage'
        elif idt == 'direct':
            return 'Directional'
        else:
            print('Wrong input! Please try again ...')


def input_threshold() -> [int]:
        """ Input threshold for BUY and SELL """
        while True:
            buy = int(input('BUY THRESHOLD = '))
            sell = int(input('SELL THRESHOLD = '))

            if buy <= sell:
                print('BUY threshold need to be greater than SELL threshold! Please try again ...\n ')
            else:
                return [buy, sell]


def _input_numday() -> int:
    """ Input the number of days for indicator to analysis """

    while True:
        numday = int(input('Number of date for indicator = '))
        if numday < 1:
            print('Number of days need to be >= 1. Please try again ... ')
        else:
            return numday





def _debug_print_table(table: [indicators_module.Stock]) -> None:
    """ Only use to show debug calculation  """
    print('\n\t{:10s}    {:6s}    {:6}    {:9s}  {:6s}'.format('DATE','CLOSE','CHANGE','INDICATOR','SIGNAL'))

    for i in table:
        print('\t{:10s}    {:6.2f}    {:6}    {:9.2f}  {:6s}'.format(i.date,i.price,i.change,i.indicator,i.signal))



def _print_table(table: [indicators_module.Stock], symbol: str, indicator: str,numday: str) -> None:
    print('\n\tSYMBOL:',symbol)

    if indicator == 'SimpleMovingAverage':
        print('\tSTRATEGY: Simple moving average (' + str(numday) + '-day)')
    else:
        print('\tSTRATEGY: '+indicator+ ' (' + str(numday) + '-day)')

    print('\n\t{:10s}    {:6s}    {:9s}  {:6s}'.format('DATE','CLOSE','INDICATOR','SIGNAL'))
    for i in table:
        print('\t{:10s}    {:6.2f}    {:9.2f}  {:6s}'.format(i.date,i.price,i.indicator,i.signal))





if __name__ == '__main__':
    while True:
        symbol = _input_symbol()

        if len(symbol) == 0:
            print('\nProgram exits.')
            break

        else:
            url = _input_date_range(symbol)
            # print(url)  # debug

            dl_datalist = download_module.download_and_decode_data(url)
            data_table = indicators_module.Table(dl_datalist)  # initialize to a new list of stock quotes

            indicator = _input_indicator()
            # print(eval('indicators_module.'+indicator+'(data_table)')) # debug
            num_days = _input_numday()

            indicator_table = indicators_module.run_calculations(eval('indicators_module.'+indicator+'(data_table)'), num_days)
            # _debug_print_table(indicator_table)  # debug
            signal_table = signals_module.execute_strategies(eval('signals_module.'+indicator+'(indicator_table)'), num_days)
            # _debug_print_table(signal_table)  # debug

            _print_table(indicator_table, symbol, indicator, num_days)

            print('\nAnalysis completed. Program exits.')
            break
