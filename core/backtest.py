from core.data import Data

class Backtest(Data):
    """
    Should take in the portfolio tickers, strategy class, start and end time
    then return the percent change over that time

    Attributes:
        portfolio (:obj:`Portfolio`): Portfolio object
        strategy(:obj:`Strategy`): strategy implemented in backtest
        data (:obj:`pd.DataFrame`): price data for given stocks for a given time step
    """

    def __init__(self, portfolio, strategy, data):
        self.portfolio = portfolio
        self.strategy = strategy
        self.data = data

    def run(self):
        pass


    def step(self):
        pass
