from pull_data import HistoricDataSession
import pandas as pd
import os

class Analysis(HistoricDataSession):
    """
    Represents an object of covariance analysis. Given a portfolio, you can pull various metrics.

    Attributes:
        portfolio (:obj:`list` of :obj:`str`): a list of the ticker names

    """

    def __init__(self, portfolio = None):
        super(Analysis, self).__init__(portfolio = portfolio)
        portfolio = self.portfolio
        self.inquiry()
        cwd = os.getcwd()
        self.data = []
        for ticker in portfolio:
            items = pd.read_csv(cwd+'/saved_data/'+ticker+'.csv')
            self.data.append(items)

    def calculate_interday_difference(self):
        """
        Takes raw csv data from Google and calculates interday percentage difference

        Returns:
            change_data (:obj:`panda.Dataframe`): Percentage change interday data matrix

        """
        percent_change = []
        for items in self.data:
            items['Close'] = pd.to_numeric(items['Close'], errors='coerce')
            items['Open'] = pd.to_numeric(items['Open'], errors='coerce')
            items['Change'] = 100*(items['Close'] - items['Open']) / items['Open']
            addition = items.loc[:,['Date', 'Change']]
            addition.set_index('Date', inplace = True)
            percent_change.append(addition)

        change_data= percent_change[0]
        percent_change.pop(0)
        index = 1
        for item in percent_change:
            change_data = change_data.join(item, how='left', rsuffix=' ' + self.portfolio[index])
            index += 1
        change_data.rename(columns = {'Change': 'Change '+self.portfolio[0]}, inplace = True)
        return change_data

    def covariance_analysis(self, days):
        """
        Runs covariance analysis on a portfolio based on interday
        percent changes

        Args:
            days (:obj:`int`): Number of days to use for the data

        Returns:
            covariance_matrix (:obj:`panda.Dataframe`): Covariance Matrix of given portfolio
            normalized_covariance_matrix_to_index (:obj:`panda.Series`): Covariance compared to an index
        """

        change_data = self.calculate_interday_difference()
        covariance_matrix = change_data[0:days].cov()

        index_cov = covariance_matrix['Change '+ self.portfolio[0]]
        normalized_covariance_matrix_to_index = index_cov.divide(index_cov[0])

        return covariance_matrix, normalized_covariance_matrix_to_index


    def beta_slippage_analysis(self,days,multipliers):
        """
        Runs beta_slippage analysis on a portfolio based on interday
        percent changes for leveraged ETFs

        First entry in the portfolio is the asset the leveraged fund is compared too
        Ex. VXX and TVIX

        Args:
            days (:obj:`int`): Number of days to use for the data
            multipliers(:obj:`list`): List of the leverages in the same order of the portfolio

        Returns:
            beta_slippage_matrix (:obj:`panda.Dataframe`): Matrix of the given slippage compared to the underlying asset

        """
        change_data = self.calculate_interday_difference()

        index = 1
        slippage = pd.DataFrame()
        for mult in multipliers:
            slippage['Beta Slippage '+self.portfolio[index]] = mult*change_data['Change '+ self.portfolio[0]] - change_data['Change '+ self.portfolio[index]]
            index += 1
        return slippage

    def volitility_analysis(self,days):
        """
        Measures the volitility of each stock based on specified day amounts

        Args:
            days (:obj:`int`): Number of days to use for the data

        Returns:
            average_change(:obj:`panda.Series`): Average percentage change per day
            volitlity(:obj:`panda.Series`): Deviation percentage change per day

        """
        change_data = self.calculate_interday_difference()
        return change_data.mean(), change_data.std()


    def moving_average_analysis(self):
        """
        Measures the 50 and 200 day moving average of the stock

        Returns:
            moving_average_50(:obj:`panda.Series`): 50 day moving average
            moving_average_200(:obj:`panda.Series`): 200 day moving average
        """

        closing = pd.DataFrame()
        index = 0
        for items in self.data:
            items['Close'] = pd.to_numeric(items['Close'], errors='coerce')
            closing['Close ' + self.portfolio[index]] = items['Close']
            index += 1

        return closing.iloc[0:200].mean(), closing.iloc[0:50].mean()

    def moving_percent_change(self):
        change_data = self.calculate_interday_difference()

        return change_data.pct_change(10), change_data.pct_change(25)
