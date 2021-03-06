import pandas
import QSTK.qstkutil.qsdateutil as du
import QSTK.qstkutil.tsutil as tsu
import QSTK.qstkutil.DataAccess as da
import datetime as dt
import csv
#step1
reader=csv.reader(open("orders.csv",'rU'),delimiter=';')
dates=[]
symbols=[]
for order in reader:
    orderInfo= order[0].split(',')
    dates.append(dt.datetime(int( orderInfo[0]),int( orderInfo[1]),int(orderInfo[2])))
    symbols.append( orderInfo[3])
symbolList = list(set( symbols))
#step2
dt_start = dates[0]
dt_end = dates[-1]+dt.timedelta(days=1)
dt_timeofday = dt.timedelta(hours=16)
ldt_timestamps = du.getNYSEdays(dt_start, dt_end, dt_timeofday)
c_dataobj = da.DataAccess('Yahoo')
ls_keys = ['close']
ldf_data = c_dataobj.get_data(ldt_timestamps, symbolList, ls_keys)
d_data = dict(zip(ls_keys, ldf_data))
#Step3
tradeMatrix = pandas.DataFrame(index=ldt_timestamps,columns=symbolList).fillna(0)
reader=csv.reader(open("orders.csv",'rU'),delimiter=';')
for order in reader:
    orderInfo= order[0].split(',')
    orderDate = dt.datetime(int( orderInfo[0]),int( orderInfo[1]),int(orderInfo[2]))
    for marketDay, numberTraded in tradeMatrix.iterrows():
        if marketDay._date_repr ==orderDate.strftime('%Y-%m-%d'):
            amount=0
            if  orderInfo[4]=='Buy':
                amount = int(orderInfo[5])
            else:
                amount = - int(orderInfo[5])
            numberTraded[orderInfo[3]] = amount
print tradeMatrix
#step4 
cash = pandas.Series(0, index=ldt_timestamps)
for marketDay, orderValues in tradeMatrix.iterrows():
    cash.ix[marketDay]+=orderValues*d_data['close'].ix[marketDay]
print cash
i=1



