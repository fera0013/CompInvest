#Module containing code to read in and convert stock and asset related  date
#imports
# QSTK Imports
import QSTK.qstkutil.qsdateutil as du
import QSTK.qstkutil.tsutil as tsu
import QSTK.qstkutil.DataAccess as da

# Third Party Imports
import datetime as dt
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import time
from scipy.optimize import minimize

def ReadData(startDate, endDate, ls_symbols,ls_data=['open', 'high', 'low', 'close', 'volume', 'actual_close'],str_DataSource='Yahoo'):
    #Create datetime objects for Start and End dates (STL)

    #Initialize daily timestamp: closing prices, so timestamp should be hours=16 (STL)
    dt_timeofday = dt.timedelta(hours=16);

    #Get a list of trading days between the start and end dates (QSTK)
    ldt_timestamps = du.getNYSEdays(startDate, endDate, dt_timeofday);

    #Create an object of the QSTK-dataaccess class with Yahoo as the source (QSTK)
    c_dataobj = da.DataAccess(str_DataSource, cachestalltime=0);

    #Read the data and map it to ls_keys via dict() (i.e. Hash Table structure)
    ldf_data = c_dataobj.get_data(ldt_timestamps, ls_symbols, ls_data);
    d_data = dict(zip(ls_data, ldf_data));

    return [d_data, startDate, endDate, dt_timeofday, ldt_timestamps];