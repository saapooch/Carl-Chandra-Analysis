from analysis.analysis import Analysis
import unittest

class TestAnalysis(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        self.cov = Analysis(portfolio = ['SPY' ,'SPXL', 'SPXS'])

    def test_calculate_interday_difference(self):
        data = self.cov.calculate_interday_difference()
        self.assertEqual(len(data.columns), 3)

    def test_covariance_analysis(self):
        covariance_matrix, normalized_covariance_matrix_to_index = self.cov.covariance_analysis(100)
        self.assertEqual(covariance_matrix.shape, (3, 3))
        self.assertEqual,(len(normalized_covariance_matrix_to_index), 3)


    def test_beta_slippage_analysis(self):
        data = self.cov.beta_slippage_analysis(50, [3,-3])


    def test_volitility_analysis(self):
        average, volitility = self.cov.volitility_analysis(50)

    def test_moving_average_analysis(self):
        moving_average_200, moving_average_50 = self.cov.moving_average_analysis()
