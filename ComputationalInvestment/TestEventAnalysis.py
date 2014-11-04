import unittest
import EventAnalyzer
import datetime as dt
import MarketSimulator
import PortfolioOptimizer
import QSTK.qstkutil.qsdateutil as du
import QSTK.qstkutil.DataAccess as da
import QSTK.qstkstudy.EventProfiler as ep

class Test_EventAnalysis(unittest.TestCase):
    def test_EventMatrixCreation(self):
        #Reference data fromhttp://wiki.quantsoftware.org/index.php?title=CompInvestI_Homework_2
        expectedNumberOfEvents=180
        dt_start = dt.datetime(2008, 1, 1)
        dt_end = dt.datetime(2009, 12, 31)
        ldt_timestamps = du.getNYSEdays(dt_start, dt_end, dt.timedelta(hours=16))
        dataobj = da.DataAccess('Yahoo')
        ls_symbols = dataobj.get_symbols_from_list('sp5002012')
        ls_symbols.append('SPY')
        ls_keys = ['open', 'high', 'low', 'close', 'volume', 'actual_close']
        ldf_data = dataobj.get_data(ldt_timestamps, ls_symbols, ls_keys)
        d_data = dict(zip(ls_keys, ldf_data))
        for s_key in ls_keys:
            d_data[s_key] = d_data[s_key].fillna(method='ffill')
            d_data[s_key] = d_data[s_key].fillna(method='bfill')
            d_data[s_key] = d_data[s_key].fillna(1.0)
        [numberOfEvents,df_events] = EventAnalyzer.CreateEventMatrix(ls_symbols, d_data,5)
        self.assertEqual(expectedNumberOfEvents, numberOfEvents)

    def test_BollingerEventMatrixCreation(self):
        #Reference data fromhttp://wiki.quantsoftware.org/index.php?title=CompInvestI_Homework_2
        expectedNumberOfEvents=295
        dt_start = dt.datetime(2008, 1, 1)
        dt_end = dt.datetime(2009, 12, 31)
        ldt_timestamps = du.getNYSEdays(dt_start, dt_end, dt.timedelta(hours=16))
        dataobj = da.DataAccess('Yahoo')
        ls_symbols = dataobj.get_symbols_from_list('sp5002012')
        ls_symbols.append('SPY')
        ls_keys = ['open', 'high', 'low', 'close', 'volume', 'actual_close']
        ldf_data = dataobj.get_data(ldt_timestamps, ls_symbols, ls_keys)
        d_data = dict(zip(ls_keys, ldf_data))
        for s_key in ls_keys:
            d_data[s_key] = d_data[s_key].fillna(method='ffill')
            d_data[s_key] = d_data[s_key].fillna(method='bfill')
            d_data[s_key] = d_data[s_key].fillna(1.0)
        [numberOfEvents,df_events] = EventAnalyzer.FindBollingerEvents(  ls_symbols,  dt_start,dt_end,loopBackPeriod=20)
        ep.eventprofiler(df_events, d_data, i_lookback=20, i_lookforward=20,
            s_filename='BollingerEventStudy.pdf', b_market_neutral=True, b_errorbars=True,
            s_market_sym='SPY')
        self.assertEqual(expectedNumberOfEvents,numberOfEvents)

    def test_EventBasedOrderGeneration(self):
        finalPortfolioValue = 54824
        startDate = dt.datetime(2008, 1, 1)
        endDate = dt.datetime(2009, 12, 31)
        orderFile= 'eventBasedOrders.csv'
        EventAnalyzer.GenerateEventBasedTradingOrders('sp5002012', 
                                        startDate, 
                                        endDate,
                                        5,
                                        100,
                                        5,
                                        orderFile)
        portfolioValues = MarketSimulator.SimulateMarket(50000,  orderFile,startDate,endDate)
        self.assertAlmostEqual(finalPortfolioValue,portfolioValues.tail(1).ix[0])
    def test_SharpeRatioOfEventBasedOrdersPortfolio(self):
        startDate = dt.datetime(2008, 1, 1)
        endDate = dt.datetime(2009, 12, 31)
        orderFile= 'eventBasedOrders.csv'
        expectedLowerSharpeBoundary=0.95
        expectedUpperSharpeBoundary=1.05
        EventAnalyzer.GenerateEventBasedTradingOrders('sp5002012', 
                                        startDate, 
                                        endDate,
                                        8,
                                        100,
                                        5,
                                        orderFile)
        portfolioValues = MarketSimulator.SimulateMarket(50000,  orderFile,startDate,endDate)
        portfolioStatistics = PortfolioOptimizer.calculatePortfolioStatistics(portfolioValues.tolist())
        sharpeRatio=portfolioStatistics[2]
        self.assertGreater(sharpeRatio,  expectedLowerSharpeBoundary)
        self.assertLess(sharpeRatio,  expectedUpperSharpeBoundary)
    def test_TotalReturnOfEventBasedOrdersPortfolio(self):
        startDate = dt.datetime(2008, 1, 1)
        endDate = dt.datetime(2009, 12, 31)
        orderFile= 'eventBasedOrders.csv'
        expectedLowerReturnBoundary=1.2
        expectedUpperReturnBoundary=1.3
        initialInvestment=50000
        EventAnalyzer.GenerateEventBasedTradingOrders('sp5002012', 
                                        startDate, 
                                        endDate,
                                        9,
                                        100,
                                        5,
                                        orderFile)
        portfolioValues = MarketSimulator.SimulateMarket(initialInvestment,  orderFile,startDate,endDate)
        totalReturn=portfolioValues.tail(1).ix[0]/initialInvestment
        self.assertGreater(totalReturn,  expectedLowerReturnBoundary)
        self.assertLess(totalReturn,  expectedUpperReturnBoundary)

    def test_BollingerEventBasedOrders(self):
        #Reference values from http://wiki.quantsoftware.org/index.php?title=CompInvesti_Homework_7
        startDate = dt.datetime(2008, 1, 1)
        endDate = dt.datetime(2009, 12, 31)
        orderFile= 'BollingerEventBasedOrders.csv'
        initialInvestment=100000
        expectedSharpeRatioOfFund = 0.878184607953
        expectedSharpeRatioOfSPX = -0.119678949254
        expectedTotalReturnOfFund= 1.09201 
        expectedTotalReturnOfSPX = 0.821125528503
        expectedStandardDeviationOfFund =  0.00351096966115
        expectedStandardDeviationOfSPX = 0.0224380004349
        averageDaiReturnOfFund =  0.000194228352864
        averageDailyReturnOfSPX = -0.000169161547432
        dataobj = da.DataAccess('Yahoo')
        ls_symbols = dataobj.get_symbols_from_list('sp5002012')
        EventAnalyzer.GenerateBollingerEventsBasedOrders(ls_symbols, 
                                        startDate, 
                                        endDate,
                                        20,
                                        100,
                                        5,
                                        orderFile)
        portfolioValues = MarketSimulator.SimulateMarket(initialInvestment,  orderFile,startDate,endDate)
        portfolioStatistics = PortfolioOptimizer.calculatePortfolioStatistics(portfolioValues.tolist())
        sharpeRatio=portfolioStatistics[2]
        standardDeviation=portfolioStatistics[0]
        #Compare only up to the first post-decimal, to ignore minor differenced caused by float implementation differences     
        self.assertEqual(int(expectedSharpeRatioOfFund*10),  int(sharpeRatio*10))
        self.assertEqual(int(expectedStandardDeviationOfFund*1000),  int( standardDeviation*1000))
if __name__ == '__main__':
    unittest.main()
