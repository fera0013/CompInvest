import unittest
import CIHomework3
import pandas
from pandas.util.testing import assert_frame_equal

class Test_TestCIHomework3(unittest.TestCase):
    def test_MarketSimulator(self):
        expectedFinalValueOrders=[2011,12,20,1133860]
        expectedFinalValueOrders2=[2011,12,14, 1078753]
        values = CIHomework3.marketsim(1000000,"orders.csv")
        assert_frame_equal(xpectedFinalValueOrders, values[-1])
        values = CIHomework3.marketsim(1000000,"orders2.csv")
        assert_frame_equal(expectedFinalValueOrders2, values[-1])
      
         
if __name__ == '__main__':
    unittest.main()
