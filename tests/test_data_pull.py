import unittest
from core.data_pull import RealTimeDataSession, HistoricDataSession

class TestRealTime(unittest.TestCase):
    def test_inquiry(self):
        r = RealTimeDataSession(portfolio = 'ZYNE', sampling = 50, islive = True)
        text = r.pull_text()
        stat = r.stat_inquiry(text)
        price = r.price_inquiry(text)
        self.assertIsInstance(price[6], str)
        self.assertIsInstance(price[7], float)

    def test_run_real_time(self):
        z = RealTimeDataSession(portfolio = 'ZYNE', sampling = 1, islive = True, max_time = 3, fname = 'real_time_test.csv' )
        n = z.run_real_time()
        self.assertEqual(n, 'Done.')

class TestHistoric(unittest.TestCase):
    def test_inquiry(self):
        h = HistoricDataSession(portfolio='VXX', fname = 'historical_test.csv')
        data = h.inquiry()
        self.assertIsInstance(data[5][2], float)
