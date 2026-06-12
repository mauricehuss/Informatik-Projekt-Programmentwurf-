class FeeCalculator:
    def __init__(self):
        self.fixed_fee = 5.0
        self.percent_fee = 0.005

    def calculate_fee(self, value):
        return self.fixed_fee + value * self.percent_fee
    