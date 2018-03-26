from analysis.analysis import Analysis
import pandas as pd
import matplotlib
matplotlib.use('TkAgg')
import matplotlib.pyplot as plt


class Portfolio(Analysis):

    def __init__(self, portfolio = None, stocks = None, init_value = None):

        super(Portfolio, self).__init__(portfolio = portfolio)

        self.portfolio = portfolio
        self.stocks = stocks
        self.init_value = init_value


    def returns(self):

        init_total = sum([na*nb for na,nb in zip(self.stocks,self.init_value)])

        days = 200
        closing = pd.DataFrame()
        index = 0
        for items in self.data:
            items['Close'] = pd.to_numeric(items['Close'], errors='coerce')
            closing['Close ' + self.portfolio[index]] = items['Close']
            index += 1

        total_over_time = []
        horizon = []
        for i in range(days):
            total_over_time.append(sum([na*nb for na,nb in zip(self.stocks,closing.loc[i].tolist())]))
            horizon.append(init_total)

        fig = plt.figure()
        plt.plot(range(days), total_over_time)
        plt.plot(range(days), horizon)
        fig.savefig('temp.png')
