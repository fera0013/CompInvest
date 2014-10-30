import PortfolioOptimizer
import pandas

def CalculateBollingerBands(symbols,startDate,EndDate,loopBackPeriod):
    data = PortfolioOptimizer.ReadData(startDate,EndDate,symbols)
    price = data[0]['close']
    for symbol in price.columns:
        price[symbol]=(price[symbol]-pandas.rolling_mean( price[symbol],loopBackPeriod))/pandas.rolling_std(price[symbol],loopBackPeriod)
    return price



