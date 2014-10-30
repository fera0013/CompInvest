import unittest
import pandas
import datetime
import TechnicalIndicators
from pandas.util.testing import assert_frame_equal

class Test_TestBollingerBands(unittest.TestCase):
    def test_BollingerBandImplementation(self):
        expectedBollingerValues=pandas.DataFrame(data={'AAPL':[1.185009,1.371298,1.436278,1.464894,0.793493],
                                                       'GOOG':[1.298178,1.073603,0.745548,0.874885,0.634661],
                                                       'IBM':[1.177220,0.590403,0.863406,2.096242,1.959324],
                                                       'MSFT':[1.237684,0.932911,0.812844,0.752602,0.498395]},
                                                 index=[datetime.datetime(2010,12,23,16),
                                                        datetime.datetime(2010,12,27,16),
                                                        datetime.datetime(2010,12,28,16),
                                                        datetime.datetime(2010,12,29,16),
                                                        datetime.datetime(2010,12,30,16)])
        symbols=['AAPL','GOOG','IBM','MSFT']
        startDate=datetime.datetime(2010,1,1)
        endDate=datetime.datetime(2010,12,31)
        loopbackPeriod=20
        calculatedBollingerValues = TechnicalIndicators.CalculateBollingerBands(symbols,startDate,endDate,loopbackPeriod)
        pandas.util.testing.assert_frame_equal(expectedBollingerValues,calculatedBollingerValues.tail(5),check_less_precise=True)
        questionOneDate  = datetime.datetime( 2010,5,21,16)
        questionTwoDate  = datetime.datetime( 2010,6,14,16)
        print calculatedBollingerValues.loc[questionOneDate]['AAPL']
        print calculatedBollingerValues.loc[questionTwoDate]['MSFT']
if __name__ == '__main__':
    unittest.main()
