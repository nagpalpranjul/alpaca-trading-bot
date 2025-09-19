from alpaca_trade_api.rest import REST
import yfinance as yf

# Alpaca credentials
API_KEY = 'https://paper-api.alpaca.markets/v2'
API_SECRET = 'PA32VKLQNSMA'
BASE_URL = 'https://paper-api.alpaca.markets'
api = REST(API_KEY, API_SECRET, BASE_URL)

# Strategy settings
tickers = ['AAPL', 'MSFT', 'GOOGL']
buy_trigger = -0.05
sell_trigger = 0.10
buy_amount = 5
sell_amount = 10
portfolio = {t: {'last_price': None, 'position': 0} for t in tickers}

# Run strategy
for ticker in tickers:
    data = yf.download(ticker, period='1y')['Close']

    for price in data:
        last_price = portfolio[ticker]['last_price']
        if last_price is None:
            portfolio[ticker]['last_price'] = price
            continue

        change_pct = (price - last_price) / last_price

        if change_pct <= buy_trigger:
            qty = round(buy_amount / price, 4)
            api.submit_order(symbol=ticker, qty=qty, side='buy', type='market', time_in_force='gtc')
            portfolio[ticker]['last_price'] = price
            portfolio[ticker]['position'] += qty

        elif change_pct >= sell_trigger and portfolio[ticker]['position'] * price >= sell_amount:
            qty = round(sell_amount / price, 4)
            api.submit_order(symbol=ticker, qty=qty, side='sell', type='market', time_in_force='gtc')
            portfolio[ticker]['last_price'] = price
            portfolio[ticker]['position'] -= qty
