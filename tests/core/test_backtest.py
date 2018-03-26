import unittest
from core.backtest import BacktestSession
from core.assets import Portfolio

class TestBacktest(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        stocks = {'AAPL': 5, 'SPXL': 10, 'SOXL':50, 'SPY': 20}
        self.port = Portfolio(stocks = stocks)
        self.backtest_session = BacktestSession(portfolio=self.port)


    def test_collect_data(self):
        self.backtest_session.collect_data()
        self.backtest_session.run_backtest()
        print(self.backtest_session.log)
