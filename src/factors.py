import pandas as pd

def compute_momentum(prices):
    monthly = prices.resample('ME').last()
    momentum = monthly.pct_change(12).shift(1)
    return momentum

if __name__ == "__main__":
    from data_loader import load_all_prices
    prices = load_all_prices()
    momentum = compute_momentum(prices)
    print(momentum.tail())
    print(momentum.shape)