class Decision(object):

    def __init__(self, action, error):
        self.action = action
        self.error = error

    def __repr__(self):
        return 'Decision(%s, %s)' % (self.action, self.error)


class BaseStrategy(object):

    """
    input (obj:depends): data to make decision on (prices in this case)

    """
    def __init__(self, input):
        self.input = input
        self.decision = Decision(None, None)

    def get_decision(self):
        return self.decision
