import pandas
import datetime as dt
import QSTK.qstkutil.qsdateutil as du
import numpy as np

def marketsim(initialInvestment,orderPath):
    #parseDate = lambda y,m,d: datetime.datetime(y,m,d)
    order = pandas.DataFrame.from_csv(orderPath, index_col=False,header=None, parse_dates=[[0,1,2]])#date_parser=parseDate)
    oderDates = order.iloc[:,0]
    # We need closing prices so the timestamp should be hours=16.
    dt_timeofday = dt.timedelta(hours=16)
    dateBoundaries = du.getNYSEdays( oderDates[0] , oderDates[oderDates.size-1], dt_timeofday)
    for date in dateBoundaries:
       orderData = order.ix[oderDates[0] == date]
       if orderData:
           i=orderData
    
      
  