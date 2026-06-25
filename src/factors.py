import yfinance as yf
import pandas as pd

def compute_momentum(prices):
    monthly = prices.resample('ME').last()
    momentum = monthly.pct_change(12).shift(1)
    return momentum

def compute_volatility(prices):
    daily = prices.pct_change()
    volatility = daily.rolling(252).std() * 252**0.5
    return volatility

def compute_value(tickers):
    pe_ratios = {}
    for ticker in tickers:
        info = yf.Ticker(ticker).info
        pe = info.get('trailingPE')
        pe_ratios[ticker] = pe
    pe_series = pd.Series(pe_ratios)
    pe_series = pe_series.fillna(pe_series.median())
    pe_series = -pe_series
    return pe_series

if __name__ == "__main__":
    from data_loader import load_all_prices, SP100_TICKERS
    prices = load_all_prices()
    momentum = compute_momentum(prices)
    volatility = compute_volatility(prices)
    value = compute_value(SP100_TICKERS)
    print(value.head(10))
    print(f"Missing P/E values: {value.isnull().sum()}")
    print(f"Negative P/E values: {(value < 0).sum()}")