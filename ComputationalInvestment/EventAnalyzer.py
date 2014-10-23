'''
(c) 2011, 2012 Georgia Tech Research Corporation
This source code is released under the New BSD license.  Please see
http://wiki.quantsoftware.org/index.php?title=QSTK_License
for license details.

Created on January, 23, 2013

@author: Sourabh Bajaj
@contact: sourabhbajaj@gatech.edu
@summary: Event Profiler Tutorial
'''


import pandas as pd
import numpy as np
import math
import copy
import QSTK.qstkutil.qsdateutil as du
import datetime as dt
import QSTK.qstkutil.DataAccess as da
import QSTK.qstkutil.tsutil as tsu
import QSTK.qstkstudy.EventProfiler as ep
import csv

"""
Accepts a list of symbols along with start and end date
Returns the Event Matrix which is a pandas Datamatrix
Event matrix has the following structure :
    |IBM |GOOG|XOM |MSFT| GS | JP |
(d1)|nan |nan | 1  |nan |nan | 1  |
(d2)|nan | 1  |nan |nan |nan |nan |
(d3)| 1  |nan | 1  |nan | 1  |nan |
(d4)|nan |  1 |nan | 1  |nan |nan |
...................................
...................................
Also, d1 = start date
nan = no information about any event.
1 = status bit(positively confirms the event occurence)
"""


def find_events(ls_symbols, d_data,eventThreshold):
    ''' Finding the event dataframe '''
    df_close = d_data['actual_close']
    ts_market = df_close['SPY']

    print "Finding Events"

    # Creating an empty dataframe
    df_events = copy.deepcopy(df_close)
    df_events = df_events * np.NAN

    # Time stamps for the event range
    ldt_timestamps = df_close.index

    for s_sym in ls_symbols:
        for i in range(1, len(ldt_timestamps)):
            # Calculating the returns for this timestamp
            f_symprice_today = df_close[s_sym].ix[ldt_timestamps[i]]
            f_symprice_yest = df_close[s_sym].ix[ldt_timestamps[i - 1]]
         
            # Event is found if the symbol is down more then 3% while the
            # market is up more then 2%
            if  f_symprice_yest>= eventThreshold and   f_symprice_today < eventThreshold:
                df_events[s_sym].ix[ldt_timestamps[i]] = 1

    return df_events


def GenerateEventBasedTradingOrders(ls_symbols,
                                    startDate,
                                    endData,
                                    eventThreshold,
                                    numberOfSharesToBuy,
                                    numberOfDaysToHold,
                                    orderFile):
    ldt_timestamps = du.getNYSEdays(startDate, endData, dt.timedelta(hours=16))
    print "Load S&P 2012"
    dataobj = da.DataAccess('Yahoo')
    ls_symbols = dataobj.get_symbols_from_list(ls_symbols)
    ls_symbols.append('SPY')

    ls_keys = ['actual_close']
    ldf_data = dataobj.get_data(ldt_timestamps, ls_symbols, ls_keys)
    d_data = dict(zip(ls_keys, ldf_data))

    for s_key in ls_keys:
        d_data[s_key] = d_data[s_key].fillna(method='ffill')
        d_data[s_key] = d_data[s_key].fillna(method='bfill')
        d_data[s_key] = d_data[s_key].fillna(1.0)

    df_close = d_data['actual_close']
    ts_market = df_close['SPY']

    print "Finding Events"

    # Creating an empty dataframe
    df_events = copy.deepcopy(df_close)
    df_events = df_events * np.NAN

    # Time stamps for the event range
    ldt_timestamps = df_close.index
    with open(orderFile, 'wb') as csvfile:
       orderWriter = csv.writer(csvfile, delimiter=',', quoting=csv.QUOTE_MINIMAL)
       for s_sym in ls_symbols:
           for i in range(1, len(ldt_timestamps)):
            # Calculating the returns for this timestamp
            f_symprice_today = df_close[s_sym].ix[ldt_timestamps[i]]
            f_symprice_yest = df_close[s_sym].ix[ldt_timestamps[i - 1]]
            holdUntil=(i+numberOfDaysToHold) if (i+numberOfDaysToHold)<len(ldt_timestamps) else len(ldt_timestamps)-1
            if f_symprice_yest>= eventThreshold and  f_symprice_today< eventThreshold:
                orderWriter.writerow([ldt_timestamps[i].year,
                                        ldt_timestamps[i].month,
                                        ldt_timestamps[i].day,
                                        s_sym,
                                        'Buy',
                                        numberOfSharesToBuy])
                orderWriter.writerow([ldt_timestamps[holdUntil].year,
                                        ldt_timestamps[holdUntil].month,
                                        ldt_timestamps[holdUntil].day,
                                        s_sym, 
                                        'Sell', 
                                        numberOfSharesToBuy])
                

 