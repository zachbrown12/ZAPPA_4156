import yfinance as yf


class Stockdata:
    def __init__(self, ticker):
        self.stock = yf.Ticker(str(ticker)).info
        self.valid = True
        if "ask" not in self.stock or "bid" not in self.stock:
            self.valid = False

    # Get the ask price (what you can buy immediately for)
    def ask_price(self):
        if not self.valid:
            return None
        return self.stock.get("ask")

    # Get the bid price (what you can sell immediately for)
    def bid_price(self):
        if not self.valid:
            return None
        return self.stock.get("bid")
