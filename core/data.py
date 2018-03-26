from config.config import BaseConfig
from alpha_vantage.timeseries import TimeSeries
from alpha_vantage.techindicators import TechIndicators

api_key = BaseConfig.API_KEY

class Data(object):

    def __init__(self, ticker = None):
        self.ticker = ticker
        self.ts = TimeSeries(key=api_key, output_format='pandas')
        self.ti = TechIndicators(key=api_key, output_format='pandas')

    def collect_timeseries_data(self, interval ='30min'):
        """
            interval: supported values are '1min', '5min', '15min', '30min', '60min'
        """
        return self.ts.get_intraday(self.ticker, interval=interval, outputsize='full')

    def collect_daily_techindicator_data(self, indicator=None):
        """
        Indicators are: 'ad', 'adosc', 'adx', 'adxr', 'apo', 'aroon', 'aroonosc',
         'atr', 'bbands', 'bop', 'cci', 'cmo', 'dema', 'dx', 'ema', 'ht_dcperiod',
         'ht_dcphase', 'ht_phasor', 'ht_sine', 'ht_trendline', 'ht_trendmode',
         'kama', 'macd', 'macdext', 'mama', 'mfi', 'midpoint', 'midprice', 'minus_di',
         'minus_dm', 'mom', 'natr', 'obv', 'plus_di', 'plus_dm', 'ppo', 'roc', 'rocr', 'rsi',
         'sar', 'sma', 'stoch', 'stochf', 'stochrsi', 't3', 'tema', 'trange', 'trima', 'trix',
         'ultsoc', 'willr', 'wma'
        """
        return getattr(self.ti, 'get_'+indicator)(self.ticker)
