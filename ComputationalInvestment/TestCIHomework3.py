import unittest
import CIHomework3
import pandas
from pandas.util.testing import assert_frame_equal

class Test_TestCIHomework3(unittest.TestCase):
    def test_MarketSimulator(self):
        expectedFinalMaxValuePortfolio1=1135000
        expectedFinalMinValuePortfolio1=1132000
        expectedFinalMaxValuePortfolio2=1080000
        expectedFinalMinValuePortfolio2=1070000
        values = CIHomework3.SimulateMarket(1000000,"orders.csv")
        finalValue=values.tail(1).ix[0]
        self.assertLess(finalValue, expectedFinalMaxValuePortfolio1)
        self.assertGreater(finalValue, expectedFinalMinValuePortfolio1)
        values = CIHomework3.SimulateMarket(1000000,"orders2.csv")
        finalValue=values.tail(1).ix[0]
        self.assertLess(finalValue, expectedFinalMaxValuePortfolio2)
        self.assertGreater(finalValue, expectedFinalMinValuePortfolio2)
      
         
if __name__ == '__main__':
    unittest.main()
