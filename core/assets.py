

class Portfolio(object):

    """

    stocks (obj:dict): key = ticker || value = number of shares

    """
    def __init__(self, stocks, cash=None):
        self.stocks = stocks
        self.cash = cash

    def buy(self, ticker, amount):
        if ticker in self.stocks.keys():
            self.stocks[ticker] += amount
        else:
            self.stocks[ticker] = amount


    def sell(self, ticker, amount):
        if ticker in self.stocks.keys():
            if amount <= self.stocks[ticker]:
                self.stocks[ticker] -= amount
            else:
                raise ValueError('You dont have enough of that stock')
        else:
            raise ValueError('You dont have that stock')


    def execute_decisions(self, decisions):
        """
            Takes a list of decisions and executes it for the portfolio
        """

        for command in decisions:
            if command.action == 1:
                self.buy(command.ticker, command.amount)
            elif command.action == 0:
                self.sell(command.ticker, command.amount)
            else:
                raise ValueError('Unknown Decision')

    def get_value_dict(self, current_value):
        return {k : v * current_value[k] for k, v in self.stocks.items() if k in current_value}

    def get_total_value(self, current_value):
        return sum(self.get_value_dict(current_value).values())
