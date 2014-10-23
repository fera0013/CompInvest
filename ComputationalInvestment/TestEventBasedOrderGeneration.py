import unittest
import EventAnalyzer
import datetime as dt

class Test_AutomaticOrderGeneration(unittest.TestCase):
    def test_EventBasedOrderGeneration(self):
        startDate = dt.datetime(2008, 1, 1)
        endDate = dt.datetime(2009, 12, 31)
        orderFile= 'eventBasedOrders.csv'
        EventAnalyzer.GenerateEventBasedTradingOrders('sp5002012', 
                                        startDate, 
                                        endDate,
                                        100,
                                        5,
                                        orderFile)


if __name__ == '__main__':
    unittest.main()
