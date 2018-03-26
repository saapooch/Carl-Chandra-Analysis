import unittest
from strategies.base import Decision, BaseStrategy
import random

class RandomStrategy(BaseStrategy):

    """
    _input (obj:list): data to make decision on (prices in this case)

    """

    def analysis(self):
        rand = []
        for item in self.input:
            rand.append(random.random())

        if sum(rand) > 1:
            self.decision = Decision(1, sum(rand)-1)
        else:
            self.decision = Decision(0, 1-sum(rand))


class TestRandomStrategy(unittest.TestCase):

    def setUp(self):
        self.strat = RandomStrategy(input = [1, 2])

    def test_random_strat(self):
        for i in range(20):
            self.strat.analysis()
            self.assertIn(self.strat.get_decision().action, [0,1])
            self.assertLess(self.strat.get_decision().error, 1)
