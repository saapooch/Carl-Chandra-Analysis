import unittest
from core.assets import Portfolio



class TestBacktest(unittest.TestCase):

    def setUp(self):
        stocks = {'AAPL': 5, 'SPXL': 10}
        self.current_value = {'AAPL': 50.12, 'SPXL': 132.14}
        self.port = Portfolio(stocks = stocks)

    def test_buy(self):
        self.assertEqual(self.port.stocks['AAPL'], 5)
        self.port.buy('AAPL', 12)
        self.assertEqual(self.port.stocks['AAPL'], 17)
        self.port.buy('EA', 12)
        self.assertEqual(self.port.stocks['EA'], 12)


    def test_sell(self):
        self.assertEqual(self.port.stocks['AAPL'], 5)
        self.port.sell('AAPL', 5)
        self.assertEqual(self.port.stocks['AAPL'], 0)
        self.assertRaises(ValueError, self.port.sell, 'AAPL', 5)
        self.assertRaises(ValueError, self.port.sell, 'EA', 5)

    def test_get_value_dict(self):
        value_dict = self.port.get_value_dict(self.current_value)
        self.assertEqual(value_dict['AAPL'], 250.6)

        current_value = {'AAPL': 50.12, 'SPXL': 132.14, 'EA': 200}
        value_dict = self.port.get_value_dict(current_value)
        self.assertEqual(value_dict['AAPL'], 250.6)
        

    def test_total_value(self):
        total = self.port.get_total_value(self.current_value)

        self.assertEqual(total, 1571.9999999999998)
