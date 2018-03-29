from core.data import Data
import pandas as pd
import matplotlib.pyplot as plt

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

        tickers = [ticker for ticker in self.portfolio.stocks.keys()]
        tickers.append('total')

        self.log = pd.DataFrame(columns=tickers)

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
        """
            Runs the backtest by iterating through the date list
        """


        for date in self.date_list:
            entry = []
            changed_value = 0
            for key, value in self.data.items():
                # init_val = self.portfolio.stocks[key]*self.data[key].iloc[0]['4. close']
                val = self.portfolio.stocks[key]*self.data[key].loc[date]['4. close']
                entry.append([key, self.portfolio.stocks[key], val])
                # changed_value += (val-init_val)*100/(init_val)
                changed_value += val
            entry.append(changed_value)
            self.log_entry(entry, date)

                    
            if self.strategy:
                self.run_strategy(date)



    def run_strategy(self, date):
        """
        Runs strategy changing the portfolio stock amounts
        """
        decisions = self.strategy.create_decisions(date)
        self.portfolio.execute_decisions(decisions)


    def log_entry(self, entry, date):
        self.log.loc[date] = entry


    def plot_portfolio(self):

        self.log['total'].plot()
        plt.show()
