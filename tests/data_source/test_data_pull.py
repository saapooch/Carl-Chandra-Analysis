import unittest
from data_pull import RealTimeDataSession, HistoricDataSession

# class TestRealTime(unittest.TestCase):
#     def test_inquiry(self):
#         r = RealTimeDataSession(portfolio = 'ZYNE', sampling = 50, islive = True)
#         self.result = r.inquiry()
#         self.assertIsInstance(self.result[6], str)
#         self.assertIsInstance(self.result[7], float)
#
#     def test_run_real_time(self):
#         z = RealTimeDataSession(portfolio = 'ZYNE', sampling = 1, islive = True, max_time = 5, fname = 'test.txt' )
#         n = z.run_real_time()
#         self.assertEqual(n, 'Done.')

class TestHistoric(unittest.TestCase):
    def test_inquiry(self):
        h = HistoricDataSession(portfolio='ZYNE')
        result = h.inquiry()
        print result
