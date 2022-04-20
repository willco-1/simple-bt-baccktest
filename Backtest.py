from io import IncrementalNewlineDecoder
import backtrader as bt 
import datetime 
import yfinance as yf 


cerebro = bt.Cerebro()
df = yf.download("AAPL",Start='2010-01-01')
print(df)
feed = bt.feeds.PandasData(dataname=df)
cerebro.adddata(feed)

class SmaCross(bt.Strategy):
    # list of parameters which are configurable for the strategy
     params = dict(
        pfast=10,  # period for the fast moving average
        pslow=30   # period for the slow moving average
    )

     def __init__(self):
        sma1 = bt.ind.SMA(period=self.p.pfast)  # fast moving average
        sma2 = bt.ind.SMA(period=self.p.pslow)  # slow moving average
        self.crossover = bt.ind.CrossOver(sma1, sma2)  # crossover signal

     def next(self):
        if not self.position:  # not in the market
            if self.crossover > 0:  # if fast crosses slow to the upside
                self.buy()  # enter long

        elif self.crossover < 0:  # in the market & cross to the downside
            self.close()  # close long position
cerebro.broker.setcommission(commission=0.03)
cerebro.addstrategy(SmaCross)
cerebro.addsizer(bt.sizers.PercentSizer,percents=50)
cerebro.addanalyzer(bt.analyzers.AnnualReturn, _name="yearly_return")
realized_returns = cerebro.run()
cerebro.plot()  

realized_returns[0].analyzers.yearly_return.getanalysis()
