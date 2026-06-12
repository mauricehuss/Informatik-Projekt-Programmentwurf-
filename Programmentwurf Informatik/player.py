class Player:
    def __init__(self):
        self.cash = 10000.0
        self.depot = {}

    def buy_stock(self, symbol, amount, price, fee):
        total_cost = amount * price + fee

        if self.cash < total_cost:
            return False

        self.cash = self.cash - total_cost

        if symbol in self.depot:
            self.depot[symbol] = self.depot[symbol] + amount
        else:
            self.depot[symbol] = amount

        return True

    def sell_stock(self, symbol, amount, price, fee):
        if symbol not in self.depot:
            return False

        if self.depot[symbol] < amount:
            return False

        money_back = amount * price - fee
        self.cash = self.cash + money_back

        self.depot[symbol] = self.depot[symbol] - amount

        if self.depot[symbol] == 0:
            del self.depot[symbol]

        return True

    def has_stock(self, symbol, amount):
        return symbol in self.depot and self.depot[symbol] >= amount