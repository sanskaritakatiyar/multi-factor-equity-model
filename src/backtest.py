import pandas as pd

def run_backtest(prices, positions):
    monthly_prices = prices.resample('ME').last()
    monthly_returns = monthly_prices.pct_change()
    portfolio_returns = (positions * monthly_returns).mean(axis=1)
    return portfolio_returns

if __name__ == "__main__":
    from data_loader import load_all_prices, SP100_TICKERS
    from factors import compute_momentum, compute_volatility, compute_value, compute_smb
    from portfolio import construct_portfolio, assign_positions

    prices = load_all_prices()
    momentum = compute_momentum(prices)
    volatility = compute_volatility(prices)
    value = compute_value(SP100_TICKERS)
    smb = compute_smb(SP100_TICKERS)
    composite = construct_portfolio(momentum, volatility, value, smb)
    positions = assign_positions(composite)

    returns = run_backtest(prices, positions)
    print(returns.tail(12))