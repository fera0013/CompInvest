import unittest
import EventAnalyzer
import datetime as dt
import MarketSimulator
import PortfolioOptimizer

class Test_EventAnalysis(unittest.TestCase):
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
if __name__ == '__main__':
    unittest.main()
