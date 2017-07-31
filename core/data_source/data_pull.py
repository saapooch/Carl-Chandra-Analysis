import time, os, re, csv
import requests


class RealTimeDataSession:

    def __init__(self, portfolio = 'AAPL', sampling = 10, islive = False,  max_time = 100 , fname = 'stock.txt'):
        self.portfolio = portfolio
        self.sampling = sampling
        self.islive = islive
        self.max_time = max_time
        self.fname = fname

## TODO: Add more variables and make it able for multiple portfolio
    def inquiry(self):
        url = "http://www.google.com/finance?&q="
        response = requests.get(url+self.portfolio)
        txt = response.text
        k = re.finditer('id="ref_(.*?)">(.*?)<',txt)
        if k:
            pull = []
            for item in k :
                pull.append(item.group(2))
            pull[2] = pull[2].replace('%)','')
            pull[2] = pull[2].replace('(','')
            self.price = [float(pull[0]), float(pull[1]), float(pull[2])]
            t=time.localtime()    # grasp the moment of time
            self.output=[t.tm_year,t.tm_mon,t.tm_mday,t.tm_hour,  # build a list
                    t.tm_min,t.tm_sec,self.portfolio,self.price[0],self.price[1],self.price[2]]
            return self.output
        else:
            return '-'


    def run_real_time(self):
        if self.islive:
            os.path.exists(self.fname) and os.remove(self.fname)
            total_time = 0
            while total_time < self.max_time:
                with open(self.fname,'a') as f:
                    writer=csv.writer(f,dialect="excel", delimiter = '\t')
                    t = time.localtime()
                    data = self.inquiry()
                    print(data)
                    writer.writerow(data) # save data in the file
                    print total_time
                    total_time += self.sampling
                    time.sleep(self.sampling)
        f.close()
        return 'Done.'



# class HistoricDataSession:
#
#     def __init__(self, portfolio):
#         self.portfolio = portfolio
#
# # http://www.google.com/finance/historical?cid=945810642553026&startdate=Feb%209%2C%202016&enddate=Jul%2029%2C%202017&num=30&ei=lg58WZjaCdOGesaEsrAI&start=60&output=csv
#
#     def inquiry(self):
# import requests
# url = '
# response = requests.get(url)
# print response

    # def grab_data(self):
