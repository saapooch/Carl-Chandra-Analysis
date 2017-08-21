import time, os, re, csv
import requests


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


class HistoricDataSession:
    """ Represents a session collecting historical data

    Attributes:
        portfolio (:obj:`list` of :obj:`str`): a list of the ticker names
        fname (:obj:`str`): file name for saved data
    """

    def __init__(self, portfolio = None, fname = None):
        self.portfolio = portfolio
        self.fname = fname


    def inquiry(self):
        url = 'http://www.google.com/finance/historical?q='
        url2 = '&ei=njuHWfjsIsuBmAGvl4qQAw&start=30&num=30&output=csv'
        response = requests.get(url+self.portfolio+url2)
        decoded = response.content
        cr = csv.reader(decoded.splitlines(), delimiter=',')
        mylist = list(cr)
        data = []
        for item in mylist[1:len(mylist)]:
            if item[1] == '-':
                item[1] = '-'
            else:
                item[1] = float(item[1])
            if item[2] == '-':
                item[2] = '-'
            else:
                item[2] = float(item[2])
            if item[3] == '-':
                item[3] = '-'
            else:
                item[3] = float(item[3])
            item[4] = float(item[4])
            item[5] = int(item[5])
            data.append(item)
        return data

    def save_data(self):
        data = self.inquiry()
        with open(self.fname,'a') as f:
            writer=csv.writer(f,dialect="excel", delimiter = ',')
            for item in data:
                writer.writerow(item)
