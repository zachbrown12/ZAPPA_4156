from yfinance import Ticker

# Get the ask price (what you can buy immediately for)
def ask_Price(ticker):
    stockInfo = Ticker(str(ticker)).info
    if ("regularMarketPrice" not in stockInfo 
        and "ask" not in stockInfo):
        return None
    if stockInfo["ask"] == 0:
        return stockInfo["regularMarketPrice"]
    return stockInfo["ask"]

# Get the bid price (what you can sell immediately for)
def bid_Price(ticker):
    stockInfo = Ticker(str(ticker)).info
    if ("regularMarketPrice" not in stockInfo 
        and "bid" not in stockInfo):
        return None
    if stockInfo["bid"] == 0:
        return stockInfo["regularMarketPrice"]
    return stockInfo["bid"]
