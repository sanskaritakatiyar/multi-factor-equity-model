import pandas as pd

def zscore(df):
    return (df - df.mean()) / df.std()

def construct_portfolio(momentum, volatility, value, smb):
    value_monthly = pd.DataFrame(
        [value] * len(momentum),
        index=momentum.index,
        columns=momentum.columns
    )
    smb_monthly = pd.DataFrame(
        [smb] * len(momentum),
        index=momentum.index,
        columns=momentum.columns
    )
    mom_z = zscore(momentum.T).T
    vol_z = -zscore(volatility.resample('ME').last().T).T
    val_z = zscore(value_monthly.T).T
    smb_z = zscore(smb_monthly.T).T
    composite = mom_z + vol_z + val_z + smb_z
    return composite

def assign_positions(composite):
    ranks = composite.rank(axis=1, pct=True)
    positions = pd.DataFrame(0, index=ranks.index, columns=ranks.columns)
    positions[ranks > 0.8] = 1
    positions[ranks < 0.2] = -1
    return positions

if __name__ == "__main__":
    from data_loader import load_all_prices, SP100_TICKERS
    from factors import compute_momentum, compute_volatility, compute_value, compute_smb

    prices = load_all_prices()
    momentum = compute_momentum(prices)
    volatility = compute_volatility(prices)
    value = compute_value(SP100_TICKERS)
    smb = compute_smb(SP100_TICKERS)

    composite = construct_portfolio(momentum, volatility, value, smb)
    positions = assign_positions(composite)
    print(positions.tail())
    print(positions.tail().sum(axis=1))
    
    