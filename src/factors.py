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
        try:
            info = yf.Ticker(ticker).info
            pe = info.get('trailingPE')
        except Exception:
            pe = None
        pe_ratios[ticker] = pe
    pe_series = pd.Series(pe_ratios)
    pe_series = pe_series.fillna(pe_series.median())
    pe_series = -pe_series
    return pe_series

def compute_smb(tickers):
    market_caps = {}
    for ticker in tickers:
        try:
            info = yf.Ticker(ticker).info
            mc = info.get('marketCap')
        except Exception:
            mc = None
        market_caps[ticker] = mc
    mc_series = pd.Series(market_caps)
    mc_series = mc_series.fillna(mc_series.median())
    mc_series = -mc_series
    return mc_series

if __name__ == "__main__":
    from data_loader import load_all_prices, SP100_TICKERS
    prices = load_all_prices()
    momentum = compute_momentum(prices)
    volatility = compute_volatility(prices)
    value = compute_value(SP100_TICKERS)
    smb = compute_smb(SP100_TICKERS)
    print(smb.head(10))
    print(f"Missing SMB values: {smb.isnull().sum()}")