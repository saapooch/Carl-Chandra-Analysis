import random

class Decision(object):

    def __init__(self, ticker=None, action=None, amount=None, error=None):
        self.ticker = ticker
        self.action = action
        self.amount = amount
        self.error = error

    def __repr__(self):
        return 'Decision(%s, %s, %s, %s)' % (self.ticker, self.action, self.amount, self.error)


class BaseStrategy(object):

    def __init__(self, portfolio=None):
        self.portfolio = portfolio


class RandomStrategy(BaseStrategy):
    """
    A test strategy. Should take what day it is and then simply output a decision
    """

    def create_decisions(self, date):
        decisions = []

        for key,value in self.portfolio.stocks.items():
            power = random.uniform(0, 1)
            if power < .5:
                d = Decision(ticker=key, action=0, amount=5)
            else:
                d = Decision(ticker=key, action=1, amount=5)
            decisions.append(d)
        return decisions
