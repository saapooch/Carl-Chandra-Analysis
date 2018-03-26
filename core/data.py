from config.config import BaseConfig
from alpha_vantage.timeseries import TimeSeries
from alpha_vantage.techindicators import TechIndicators

api_key = BaseConfig.API_KEY

class Data(object):

    def __init__(self, ticker = None):
        self.ticker = ticker
        self.ts = TimeSeries(key=api_key, output_format='pandas')
        self.ti = TechIndicators(key=api_key, output_format='pandas')

    def collect_intraday_timeseries_data(self, interval ='30min'):
        """
            interval: supported values are '1min', '5min', '15min', '30min', '60min'
        """

        return self.ts.get_intraday(self.ticker, interval=interval, outputsize='full')

    def collect_daily_timeseries_data(self):
        return self.ts.get_daily(self.ticker, outputsize='full')

    def collect_daily_adjusted_timeseries_data(self):
        return self.ts.get_daily_adjusted(self.ticker, outputsize='full')

    def collect_weekly_timeseries_data(self):
        return self.ts.get_weekly(self.ticker)

    def collect_weekly_adjusted_timeseries_data(self):
        return self.ts.get_weekly_adjusted(self.ticker)

    def collect_monthly_timeseries_data(self):
        return self.ts.get_monthly(self.ticker)

    def collect_monthly_adjusted_timeseries_data(self):
        return self.ts.get_monthly_adjusted(self.ticker)

        #TODO: Needs to take a list as an input
    # def collect_batch_stock_quotes_timeseries_data(self):
    #     return self.ts.get_batch_stock_quotes(self.ticker)


    def collect_daily_techindicator_data(self, indicator=None, interval='daily'):
        """
        Indicators are: 'ad', 'adosc', 'adx', 'adxr', 'apo', 'aroon', 'aroonosc',
         'atr', 'bbands', 'bop', 'cci', 'cmo', 'dema', 'dx', 'ema', 'ht_dcperiod',
         'ht_dcphase', 'ht_phasor', 'ht_sine', 'ht_trendline', 'ht_trendmode',
         'kama', 'macd', 'macdext', 'mama', 'mfi', 'midpoint', 'midprice', 'minus_di',
         'minus_dm', 'mom', 'natr', 'obv', 'plus_di', 'plus_dm', 'ppo', 'roc', 'rocr', 'rsi',
         'sar', 'sma', 'stoch', 'stochf', 'stochrsi', 't3', 'tema', 'trange', 'trima', 'trix',
         'ultsoc', 'willr', 'wma'

         interval: supported values are '1min', '5min', '15min', '30min', '60min', 'daily',
                    'weekly', 'monthly' (default 'daily')

        """
        return getattr(self.ti, 'get_'+indicator)(self.ticker, interval=interval)


        'batch_stock_quotes', 'daily', 'daily_adjusted', 'intraday', 'monthly', 'monthly_adjusted', 'weekly', 'weekly_adjusted'
