import yfinance as yf
from datetime import timedelta


class Stock:
    def __init__(self, symbol, name, price):
        self.symbol = symbol
        self.name = name
        self.price = price


class Market:
    def get_stock(self, symbol, date):
        symbol = symbol.upper().strip()

        try:
            ticker = yf.Ticker(symbol)

            next_day = date + timedelta(days=1)

            data = ticker.history(
                start=date.strftime("%Y-%m-%d"),
                end=next_day.strftime("%Y-%m-%d")
            )

            if data.empty:
                return None

            price = float(data["Close"].iloc[-1])

            try:
                info = ticker.info
                name = info.get("longName", symbol)
            except Exception:
                name = symbol

            return Stock(symbol, name, price)

        except Exception:
            return None

    def get_next_trading_day(self, date):
        new_date = date + timedelta(days=1)

        while True:
            test_stock = self.get_stock("AAPL", new_date)

            if test_stock is not None:
                return new_date

            new_date = new_date + timedelta(days=1)