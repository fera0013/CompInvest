import PortfolioOptimizer
import pandas

def CalculateBollingerBands(symbols,startDate,EndDate,loopBackPeriod):
    data = PortfolioOptimizer.ReadData(startDate,EndDate,symbols)
    price = data[0]['close']
    price=(price-pandas.rolling_mean(price,loopBackPeriod))/pandas.rolling_std(price,loopBackPeriod)    
    return price



