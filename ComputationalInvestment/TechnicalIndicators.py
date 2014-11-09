import PortfolioOptimizer
import pandas

def CalculateBollingerBands(data,loopBackPeriod):
    bollingerBand=(data-pandas.rolling_mean(data,loopBackPeriod))/pandas.rolling_std(data,loopBackPeriod)    
    return bollingerBand



