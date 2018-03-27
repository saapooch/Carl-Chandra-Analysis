import unittest
from core.backtest import BacktestSession
from core.assets import Portfolio

class TestBacktest(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        stocks = {'TVIX': 600, 'APRI': 500}
        self.port = Portfolio(stocks = stocks)
        self.backtest_session = BacktestSession(portfolio=self.port)



    def test_collect_data(self):
        self.backtest_session.collect_data()
        self.backtest_session.run_backtest()
        # self.backtest_session.plot_portfolio()
