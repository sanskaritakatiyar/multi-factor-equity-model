import yfinance as yf
import pandas as pd
import sqlalchemy
import os

SP100_TICKERS = [
    "AAPL", "ABBV", "ABT", "ACN", "ADBE", "AIG", "AMD", "AMGN", "AMT", "AMZN",
    "AVGO", "AXP", "BA", "BAC", "BK", "BKNG", "BLK", "BMY", "BRK-B", "C",
    "CAT", "CHTR", "CL", "CMCSA", "COF", "COP", "COST", "CRM", "CSCO", "CVS",
    "CVX", "DE", "DHR", "DIS", "DOW", "DUK", "EMR", "EXC", "F", "FDX",
    "GD", "GE", "GILD", "GM", "GOOG", "GOOGL", "GS", "HD", "HON", "IBM",
    "INTC", "INTU", "JNJ", "JPM", "KHC", "KO", "LIN", "LLY", "LMT", "LOW",
    "MA", "MCD", "MDLZ", "MDT", "MET", "META", "MMM", "MO", "MRK", "MS",
    "MSFT", "NEE", "NFLX", "NKE", "NVDA", "ORCL", "PEP", "PFE", "PG", "PM",
    "PYPL", "QCOM", "RTX", "SBUX", "SCHW", "SO", "SPG", "T", "TGT", "TMO",
    "TMUS", "TXN", "UNH", "UNP", "UPS", "USB", "V", "VZ", "WFC", "WMT"
]

def get_price_history(ticker):
    stock = yf.Ticker(ticker)
    data = stock.history(period='5y')
    data = data['Close']
    return data

def load_all_prices():
    if os.path.exists('data/raw/prices.db'):
        return load_from_db()
    results = {}
    for ticker in SP100_TICKERS:
        results[ticker] = get_price_history(ticker)
    prices = pd.DataFrame(results)
    prices = prices.ffill()
    prices.index = prices.index.tz_localize(None)
    save_to_db(prices)
    return prices

def save_to_db(prices):
    engine = sqlalchemy.create_engine('sqlite:///data/raw/prices.db')
    prices.to_sql('prices', engine, if_exists='replace')

def load_from_db():
    engine = sqlalchemy.create_engine('sqlite:///data/raw/prices.db')
    prices = pd.read_sql('prices', engine, index_col='Date', parse_dates=['Date'])
    return prices

if __name__ == "__main__":
    prices = load_all_prices()
    print(prices.head())
    print(prices.shape)