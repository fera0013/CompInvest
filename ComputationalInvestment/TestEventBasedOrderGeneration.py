import unittest
import EventAnalyzer
import datetime as dt
import MarketSimulator

class Test_AutomaticOrderGeneration(unittest.TestCase):
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
    def test_OutputEventBasedOrderGeneration(self):
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
        portfolioValues.tail(5)
if __name__ == '__main__':
    unittest.main()
