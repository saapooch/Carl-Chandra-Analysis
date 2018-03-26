import unittest
from core import portfolio

class TestPortfolio(unittest.TestCase):


    def test_returns(self):
        self.port  = portfolio.Portfolio(portfolio = ['ATVI', 'EA', 'AAPL', 'GWPH', 'FBNC', 'SOXL', 'SPXL', 'APRI'],
                                    stocks =  [5,2,8,7,10,1,3,100],
                                    init_value = [64.49, 117.59, 155.42, 103.62, 33.22, 91.57, 35.31, 1.57])
        self.port.returns()
