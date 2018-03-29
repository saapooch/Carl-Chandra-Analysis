import unittest
from strategies.base import Decision, BaseStrategy, RandomStrategy
from core.assets import Portfolio
from core.backtest import BacktestSession
import matplotlib.pyplot as plt

class TestRandomStrategy(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        stocks = {'MU': 60, 'SPXL': 60, 'FB':20}
        self.port = Portfolio(stocks = stocks)
        self.random = RandomStrategy(portfolio = self.port)
        self.backtest_session = BacktestSession(portfolio=self.port, strategy=self.random)


        stocks1 = {'MU': 60, 'SPXL': 60, 'FB':20}
        self.port1 = Portfolio(stocks = stocks1)

        self.backtest_session1 = BacktestSession(portfolio=self.port1)



    def test_collect_data(self):
        self.backtest_session.collect_data()
        self.backtest_session.run_backtest()
        self.backtest_session1.collect_data()
        self.backtest_session1.run_backtest()

        # print(self.backtest_session.log['total'])
        # print(self.backtest_session1.log['total'])

    #     self.backtest_session.log['total'].plot()
    #     self.backtest_session1.log['total'].plot()
    #     plt.show()

    # def test_this(self):
    #     for i in range(10):
    #         stocks = {'MU': 100, 'SPXL': 100, 'FB':100}
    #         self.port = Portfolio(stocks = stocks)
    #         self.random = RandomStrategy(portfolio = self.port)
    #         self.backtest_session = BacktestSession(portfolio=self.port, strategy=self.random)
    #         self.backtest_session.collect_data()
    #         self.backtest_session.run_backtest()
    #         self.backtest_session.log['total'].plot()
    #     plt.show()
