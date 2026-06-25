import pandas as pd

def compute_momentum(prices):
    monthly = prices.resample('ME').last()
    momentum = monthly.pct_change(12).shift(1)
    return momentum

def compute_volatility(prices):
    daily = prices.pct_change()
    volatility = daily.rolling(252).std() * 252**0.5
    return volatility

if __name__ == "__main__":
    from data_loader import load_all_prices
    prices = load_all_prices()
    momentum = compute_momentum(prices)
    volatility = compute_volatility(prices)
    print(volatility.tail())
    print(volatility.shape)