import unittest
from analysis.network import Network

class TestNetwork(unittest.TestCase):

    def test_network(self):
        net = Network(portfolio = ['AAPL', 'GOOGL', 'C'])

        net.run_network()
