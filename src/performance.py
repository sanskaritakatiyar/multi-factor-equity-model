import yfinance as yf
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

def sharpe_ratio(returns):
    mean = returns.mean() * 12
    std = returns.std() * np.sqrt(12)
    return mean / std

def max_drawdown(returns):
    cumulative = (1 + returns).cumprod()
    peak = cumulative.cummax()
    drawdown = (cumulative - peak) / peak
    return drawdown.min()

def plot_cumulative_returns(returns):
    spy = yf.download('SPY', start=returns.index[0], end=returns.index[-1], interval='1mo', progress=False)
    spy_returns = spy['Close'].pct_change().dropna()
    spy_returns.index = spy_returns.index.tz_localize(None)

    strategy_cumulative = (1 + returns).cumprod()
    spy_cumulative = (1 + spy_returns).cumprod()

    plt.figure(figsize=(12, 6))
    plt.plot(strategy_cumulative.index, strategy_cumulative.values, label='Factor Strategy', color='blue')
    plt.plot(spy_cumulative.index, spy_cumulative.values, label='S&P 500 (SPY)', color='orange')
    plt.title('Cumulative Returns: Factor Strategy vs S&P 500')
    plt.xlabel('Date')
    plt.ylabel('Cumulative Return')
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.savefig('results/cumulative_returns.png')
    plt.show()

def compute_ic(composite, returns):
    future_returns = returns.shift(-1)
    ic = composite.corrwith(future_returns, axis=1)
    return ic

def icir(ic_series):
    return ic_series.mean() / ic_series.std()

if __name__ == "__main__":
    from data_loader import load_all_prices, SP100_TICKERS
    from factors import compute_momentum, compute_volatility, compute_value, compute_smb
    from portfolio import construct_portfolio, assign_positions
    from backtest import run_backtest

    prices = load_all_prices()
    monthly_prices = prices.resample('ME').last()
    monthly_returns = monthly_prices.pct_change()
    momentum = compute_momentum(prices)
    volatility = compute_volatility(prices)
    value = compute_value(SP100_TICKERS)
    smb = compute_smb(SP100_TICKERS)
    composite = construct_portfolio(momentum, volatility, value, smb)
    positions = assign_positions(composite)
    returns = run_backtest(prices, positions)
    ic = compute_ic(composite, monthly_returns)
    
    print(f"Sharpe Ratio: {sharpe_ratio(returns):.3f}")
    print(f"Max Drawdown: {max_drawdown(returns):.3f}")
    print(f"Mean IC: {ic.mean():.4f}")
    print(f"ICIR: {icir(ic):.4f}")
    plot_cumulative_returns(returns)