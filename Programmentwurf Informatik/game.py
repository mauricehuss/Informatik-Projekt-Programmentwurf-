from datetime import datetime

from player import Player
from market import Market
from fees import FeeCalculator


class Game:
    def __init__(self):
        self.player = Player()
        self.market = Market()
        self.fees = FeeCalculator()

        self.start_date = datetime(2025, 1, 2).date()
        self.current_date = self.start_date
        self.start_value = 10000.0

    def start(self):
        print("Aktienmarkt-Spiel")
        print("-----------------")
        print("Startguthaben: 10000.00 $")
        print("Startdatum:", self.current_date.strftime("%d.%m.%Y"))

        running = True

        while running:
            print()
            print("Menue")
            print("1 - Aktienkurse anzeigen")
            print("2 - Aktien kaufen")
            print("3 - Aktien verkaufen")
            print("4 - Depot anzeigen")
            print("5 - Vermoegen anzeigen")
            print("6 - Naechster Handelstag")
            print("0 - Beenden")

            choice = input("Auswahl: ")

            if choice == "1":
                self.show_stocks()
            elif choice == "2":
                self.buy_stock()
            elif choice == "3":
                self.sell_stock()
            elif choice == "4":
                self.show_depot()
            elif choice == "5":
                self.show_assets()
            elif choice == "6":
                self.next_day()
            elif choice == "0":
                running = False
            else:
                print("Ungueltige Eingabe.")

    def show_stocks(self):
        text = input("Kuerzel eingeben, getrennt mit Leerzeichen: ")
        symbols = text.split()

        if len(symbols) == 0:
            print("Keine Kuerzel eingegeben.")
            return

        for symbol in symbols:
            stock = self.market.get_stock(symbol, self.current_date)

            if stock is None:
                print(symbol.upper(), "wurde nicht gefunden.")
            else:
                print(stock.symbol, "-", stock.name, "-", self.money(stock.price))

    def buy_stock(self):
        symbol = input("Kuerzel: ").upper().strip()
        amount = self.read_amount()

        if amount is None:
            return

        stock = self.market.get_stock(symbol, self.current_date)

        if stock is None:
            print("Dieses Kuerzel existiert nicht oder hat an diesem Tag keinen Kurs.")
            return

        value = stock.price * amount
        fee = self.fees.calculate_fee(value)
        total = value + fee

        print("Das kostet dich", self.money(value), "zuzueglich", self.money(fee), "Gebuehren.")
        print("Gesamt:", self.money(total))

        answer = input("Fortfahren? Ja/Nein: ").lower()

        if answer == "ja" or answer == "j":
            success = self.player.buy_stock(symbol, amount, stock.price, fee)

            if success:
                print("Kauf erfolgreich.")
            else:
                print("Kontostand nicht ausreichend.")
        else:
            print("Kauf abgebrochen.")

    def sell_stock(self):
        symbol = input("Kuerzel: ").upper().strip()
        amount = self.read_amount()

        if amount is None:
            return

        if not self.player.has_stock(symbol, amount):
            print("Depot nicht ausreichend.")
            return

        stock = self.market.get_stock(symbol, self.current_date)

        if stock is None:
            print("Kurs konnte nicht geladen werden.")
            return

        value = stock.price * amount
        fee = self.fees.calculate_fee(value)
        result = value - fee

        print("Du bekommst", self.money(value), "abzueglich", self.money(fee), "Gebuehren.")
        print("Auszahlung:", self.money(result))

        answer = input("Fortfahren? Ja/Nein: ").lower()

        if answer == "ja" or answer == "j":
            success = self.player.sell_stock(symbol, amount, stock.price, fee)

            if success:
                print("Verkauf erfolgreich.")
            else:
                print("Verkauf nicht moeglich.")
        else:
            print("Verkauf abgebrochen.")

    def show_depot(self):
        if len(self.player.depot) == 0:
            print("Depot ist leer.")
            return

        print("Depot am", self.current_date.strftime("%d.%m.%Y"))
        print("--------------------------------------------")

        for symbol in self.player.depot:
            amount = self.player.depot[symbol]
            stock = self.market.get_stock(symbol, self.current_date)

            if stock is None:
                print(symbol, "- Kurs nicht verfuegbar")
            else:
                total_value = amount * stock.price
                print(
                    stock.symbol,
                    "|",
                    stock.name,
                    "| Menge:",
                    amount,
                    "| Einzelwert:",
                    self.money(stock.price),
                    "| Gesamtwert:",
                    self.money(total_value)
                )

    def show_assets(self):
        depot_value = self.calculate_depot_value()
        total_value = self.player.cash + depot_value
        profit = total_value - self.start_value

        days = (self.current_date - self.start_date).days

        if days == 0:
            profit_per_day = 0
        else:
            profit_per_day = profit / days

        print("Kontostand:", self.money(self.player.cash))
        print("Depotwert:", self.money(depot_value))
        print("Gesamtvermoegen:", self.money(total_value))
        print("Gewinn/Verlust gesamt:", self.money(profit))
        print("Gewinn/Verlust pro Tag:", self.money(profit_per_day))

    def next_day(self):
        self.current_date = self.market.get_next_trading_day(self.current_date)
        print("Neuer Handelstag:", self.current_date.strftime("%d.%m.%Y"))

    def calculate_depot_value(self):
        value = 0.0

        for symbol in self.player.depot:
            amount = self.player.depot[symbol]
            stock = self.market.get_stock(symbol, self.current_date)

            if stock is not None:
                value = value + amount * stock.price

        return value

    def read_amount(self):
        try:
            amount = int(input("Menge: "))

            if amount <= 0:
                print("Menge muss groesser als 0 sein.")
                return None

            return amount

        except ValueError:
            print("Bitte eine ganze Zahl eingeben.")
            return None

    def money(self, value):
        return f"{value:.2f} $"