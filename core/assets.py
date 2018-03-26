

class Portfolio(object):

    """

    stocks (obj:dict): key = ticker || value = number of shares

    """
    def __init__(self, stocks):
        self.stocks = stocks

    def buy(self, ticker, amount):
        if ticker in self.stocks.keys():
            self.stocks[ticker] += amount
        else:
            self.stocks[ticker] = amount

        return self.stocks

    def sell(self, ticker, amount):
        if ticker in self.stocks.keys():
            if amount <= self.stocks[ticker]:
                self.stocks[ticker] -= amount
            else:
                raise ValueError('You dont have enough of that stock')
        else:
            raise ValueError('You dont have that stock')

        return self.stocks

    def get_value_dict(self, current_value):
        return {k : v * current_value[k] for k, v in self.stocks.items() if k in current_value}

    def get_total_value(self, current_value):
        return sum(self.get_value_dict(current_value).values())
