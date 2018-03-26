from core.data import Data
import pandas as pd

class BacktestSession(Data):
    """
    Should take in the portfolio tickers, strategy class, start and end time
    then return the percent change over that time

    Attributes:
        portfolio (:obj:`Portfolio`): Portfolio object
        strategy(:obj:`Strategy`): strategy implemented in backtest
    """

    def __init__(self, portfolio=None, strategy=None, start='2018-02-26', end='2018-03-26'):
        self.portfolio = portfolio
        self.strategy = strategy
        self.start = start
        self.end = end
        self.log = {}

        super(BacktestSession, self).__init__()

    def collect_data(self):
        self.data = {}
        self.date_list = []
        for ticker in self.portfolio.stocks.keys():
            self.ticker = ticker
            if self.start and self.end:
                self.data[ticker] = self.collect_daily_timeseries_data()[0].loc[self.start:self.end]
                self.date_list = self.data[ticker].index.tolist()
            else:
                self.data[ticker] = self.collect_daily_timeseries_data()[0]
                self.date_list = self.data[ticker].index.tolist()

    def run_backtest(self):

        for item in self.date_list:
            entry = []
            stock_value = 0

            self.run_strategy()

            for key, value in self.data.items():
                val = self.portfolio.stocks[key]*self.data[key].loc[item]['4. close']
                entry.append([key, self.portfolio.stocks[key], val])
                stock_value += val
            entry.append(stock_value)
            self.log_entry(entry, item)

    def run_strategy(self):
        """
        Runs strategy changing the portfolio stocks
        """
        pass

    def log_entry(self, entry, date):
        self.log[date] = entry
