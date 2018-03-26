import time, os, re, csv
import requests
import pandas as pd
import quandl
from six.moves.urllib.error import HTTPError

class RealTimeDataSession:
    """ Represents a session collecting real time data

    Attributes:
        portfolio (:obj:`list` of :obj:`str`): a list of the ticker names
        sampling (:obj:`int`): time between each collection (in seconds)
        islive (:obj:`bool`): switch for live session
        max_time (:obj:`int`): Maximum amount of time queried in seconds
        fname (:obj:`str`): file name for saved data
    """

    def __init__(self, portfolio = None, sampling = 10, islive = False,  max_time = 100 , fname = None):
        self.portfolio = portfolio
        self.sampling = sampling
        self.islive = islive
        self.max_time = max_time
        self.fname = fname

    def pull_text(self):
        url = "http://www.google.com/finance?&q="
        response = requests.get(url+self.portfolio)
        return response.text

    def stat_inquiry(self, text):
        source_other = re.finditer('td class="val">(.*)', text)
        other_data = []
        for item in source_other:
            other_data.append(str(item.group(1)))
        for i in range(len(other_data)):
            if other_data[i] == '&nbsp;&nbsp;&nbsp;&nbsp;-':
                other_data[i] = 'N/A'
        return other_data

    def price_inquiry(self, text):
        source_price = re.finditer('id="ref_(.*?)">(.*?)<', text)
        price_data = []
        for item in source_price:
            price_data.append(item.group(2))
        price_data[2] = price_data[2].replace('%)','')
        price_data[2] = price_data[2].replace('(','')
        price = [float(price_data[0]), float(price_data[1]), float(price_data[2])]
        t=time.localtime()    # grasp the moment of time
        output=[t.tm_year,t.tm_mon,t.tm_mday,t.tm_hour,  # build a list
                t.tm_min,t.tm_sec,self.portfolio,price[0],price[1],price[2]]
        return output


    def run_real_time(self):
        if self.islive:
            os.path.exists(self.fname) and os.remove(self.fname)
            total_time = 0
            while total_time < self.max_time:
                with open(self.fname,'a') as f:
                    writer=csv.writer(f,dialect="excel", delimiter = ',')
                    t = time.localtime()
                    text = self.pull_text()
                    data = self.price_inquiry(text)
                    # print(data)
                    writer.writerow(data) # save data in the file
                    # print total_time
                    total_time += self.sampling
                    time.sleep(self.sampling)
        f.close()
        return 'Done.'

class HistoricDataSession(object):
    """ Represents a session collecting historical data

    Attributes:
        portfolio (:obj:`list` of :obj:`str`): a list of the ticker names
        fname (:obj:`str`): file name for saved data
    """

    def __init__(self, portfolio = None):
        self.portfolio = portfolio

    def inquiry(self):
        all_data = []
        cwd = os.getcwd()
        for tickers in self.portfolio:
            url = 'https://query1.finance.yahoo.com/v7/finance/download/'
            url2 = '?period1=1510108581&period2=1512700581&interval=1d&events=history&crumb=/JRqfKM46Lr'
            try:
                data = pd.read_csv(url+tickers+url2)
            except HTTPError:
                print(tickers + ' was not able to load')
                continue
            all_data.append(data)
        # Saves to file /cwd/saved_data/(Ticker).csv
        index = 0
        for items in all_data:
            items.to_csv(cwd+'/saved_data/' + self.portfolio[index] +'.csv')
            index += 1
        return all_data

class QuandlDataSession(object):
    """ Represents a session collecting historical data

    Attributes:
        portfolio (:obj:`list` of :obj:`str`): a list of the ticker names
    """

    def __init__(self, portfolio = None, startDate = '2010-01-01', endDate = '2016-12-31'):
        self.portfolio = portfolio
        self.startDate = startDate
        self.endDate = endDate

    def pull_data(self):
        """
        Output:
            portfolio (:obj:`dict` of :obj:`pd.Dataframe`): a dictionary of dataframes for data

        """
        #Quandl API key associated with my account
        quandl.ApiConfig.api_key = 'PASBrxyzKbVfmxh2Cyzk'

        data = {}
        for ticker in self.portfolio:
            databaseName = "EOD/" + ticker
            data[ticker] = quandl.get(databaseName, start_date=self.startDate, end_date=self.endDate)

        return data
