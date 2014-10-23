import unittest
import EventAnalyzer

class Test_AutomaticOrderGeneration(unittest.TestCase):
    def test_EventBasedOrderGeneration(self):
        def DropBelowFiveEventHasOccured(symbol,dayBeforeValue,todayValue):
            return dayBeforeValue>= 5 and   todayValue < 5
        GenerateEventBasedTradingOrders('2012 SP500', startDate, endData, DropBelowFiveEventHasOccured,100,5)

def GenerateEventBasedTradingOrders(ls_symbols, startDate, endData, eventHasOccured):
        self.fail("Not implemented")

if __name__ == '__main__':
    unittest.main()
