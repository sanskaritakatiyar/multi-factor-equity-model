import yfinance as yf

def get_price_history(ticker):
    stock = yf.Ticker(ticker)
    data = stock.history(period='5y')
    data = data['Close']
    return data

msft_data = get_price_history("MSFT")
print(msft_data.head())