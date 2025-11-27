import time
import ccxt
import os

API_KEY = os.getenv("KUCOIN_API_KEY")
API_SECRET = os.getenv("KUCOIN_API_SECRET")
API_PASSPHRASE = os.getenv("KUCOIN_API_PASSPHRASE")

FUTURES_ENABLED = os.getenv("FUTURES_ENABLED", "false").lower() == "true"
LEVERAGE = int(os.getenv("FUTURES_LEVERAGE", 5))
TRADE_MODE = os.getenv("TRADE_MODE", "spot")
DAILY_TARGET = float(os.getenv("DAILY_TARGET", 0.20))
COINS_LIMIT = int(os.getenv("COINS_LIMIT", 20))

exchange = ccxt.kucoin({
    "apiKey": API_KEY,
    "secret": API_SECRET,
    "password": API_PASSPHRASE,
    "enableRateLimit": True
})

def get_balance():
    balance = exchange.fetch_balance()
    return balance["USDT"]["free"]

def get_top_coins(limit):
    tickers = exchange.fetch_tickers()
    volumes = sorted(
        tickers.items(),
        key=lambda x: x[1].get("quoteVolume", 0),
        reverse=True
    )
    return [coin for coin, data in volumes[:limit]]

def trade_spot(coin):
    print(f"🔵 Spot trade on {coin}")
    return True

def trade_futures(coin):
    print(f"🟠 Futures trade {coin} with {LEVERAGE}x leverage")
    return True

def main():
    start_balance = get_balance()
    print(f"💰 Start Balance: {start_balance} USDT")

    while True:
        current_balance = get_balance()
        profit = (current_balance - start_balance) / start_balance

        print(f"📊 Profit: {profit * 100:.2f}%")

        if profit >= DAILY_TARGET:
            print("🎉 DAILY TARGET REACHED! Stopping bot!")
            break

        coins = get_top_coins(COINS_LIMIT)

        for coin in coins:
            if TRADE_MODE == "spot":
                trade_spot(coin)
            elif TRADE_MODE == "hybrid":
                trade_spot(coin)
                if FUTURES_ENABLED:
                    trade_futures(coin)

        time.sleep(5)

if __name__ == "__main__":
    main()
