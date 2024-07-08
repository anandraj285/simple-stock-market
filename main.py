import json
from stock_market import StockMarket
import logging
from models.common import TradeType

def main():
    # Read stock data from JSON file
    with open('./data/stock_data.json', 'r') as f:
        stock_data = json.load(f)

    # Instantiate StockMarket
    market = StockMarket()

    # Hydrate the market with stock data
    market.get_stocks(stock_data)

    # Record some trades
    try:
        market.record_trade(stock_symbol="TEA", quantity=100, trade_type=TradeType.BUY, price=100)
        market.record_trade(stock_symbol="POP", quantity=150, trade_type=TradeType.SELL, price=120)
        market.record_trade(stock_symbol="ALE", quantity=200, trade_type=TradeType.BUY, price=50)
        market.record_trade(stock_symbol="GIN", quantity=100, trade_type=TradeType.SELL, price=90)
        market.record_trade(stock_symbol="JOE", quantity=100, trade_type=TradeType.BUY, price=130)
        market.record_trade(stock_symbol="JOE", quantity=130, trade_type=TradeType.SELL, price=130)
    except Exception as e:
        logging.error(f"Error recording trades: {e}")

    print(f"total trades : {json.dumps(market.get_trade_details(),indent=4)} ")
    # Calculate and print outputs
    print("Dividend Yield:")
    for symbol, stock in market.stocks.items():
        try:
            dy = stock.calculate_dividend_yield(100)
            print(f"{symbol}: {dy:.2f}")
        except ValueError as e:
            print(f"{symbol}: {str(e)}")

    print("\nPE Ratio:")
    for symbol, stock in market.stocks.items():
        try:
            pe = stock.calculate_pe_ratio(100)
            print(f"{symbol}: {pe:.2f}")
        except ValueError as e:
            print(f"{symbol}: {str(e)}")

    print("\nVolume Weighted Stock Price:")
    for symbol in market.stocks:
        vwsp = market.calculate_volume_weighted_stock_price(symbol)
        print(f"{symbol}: {vwsp:.2f}")

    print("\nGBCE All Share Index:")
    gbce = market.calculate_gbce_all_share_index()
    print(f"{gbce:.2f}")

if __name__ == '__main__':
    main()