import unittest
from core.data import Data

class TestData(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        self.dat = Data(ticker='SPXL')

    def test_time_series_data(self):
        self.dat.collect_intraday_timeseries_data()
        pass

    def test_collect_daily_techindicator_data(self):
        data, meta = self.dat.collect_daily_techindicator_data(indicator='stoch')
        pass

    def test_collect_monthly(self):
        data, meta = self.dat.collect_monthly_adjusted_timeseries_data()
        pass
