import unittest



class TestBacktest(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        self.portfolio = ['AAPL', 'SPY']
        self.start_time = None
        self.end_time = None

    
