import unittest
from core.data import Data

class TestData(unittest.TestCase):

    def test_alpha_vantage(self):
        dat = Data(ticker='SPXL')
        data, meta = dat.collect_daily_techindicator_data(indicator='sma')
        print(data)
