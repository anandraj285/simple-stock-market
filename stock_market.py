from models.trade import Trade
from models.stock import Stock, CommonStock, PreferredStock
from models.common import StockType, TradeType
from datetime import datetime, timedelta, timezone
from math import log, exp
from typing import Dict, List, Union
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class StockMarket:
    """
    Represents a stock market.

    Attributes:
        trades (List[Trade]): A list of trades recorded in the stock market.
        stocks (Dict[str, Stock]): A dictionary of stocks available in the market, with stock symbols as keys.

    Methods:
        record_trade: Records a trade in the stock market.
        calculate_volume_weighted_stock_price: Calculates the volume weighted stock price for a given stock symbol.
        calculate_gbce_all_share_index: Calculates the GBCE All Share Index.
        hydrate_stocks: Hydrates the stock market with stock data.
        get_trade_details: Retrieves the details of all trades recorded in the stock market.
    """

    def __init__(self):
        self.trades: List[Trade] = []
        self.stocks: Dict[str, Stock] = {}

    def record_trade(self, stock_symbol: str, quantity: int, trade_type: TradeType, price: float) -> None:
        """
        Records a trade in the stock market.

        Args:
            stock_symbol (str): The symbol of the stock being traded.
            quantity (int): The quantity of stocks being traded.
            trade_type (TradeType): The type of trade (BUY or SELL).
            price (float): The price at which the trade is executed.

        Raises:
            ValueError: If the stock symbol is not found in the market.

        Returns:
            None
        """
        try:
            stock = self.stocks.get(stock_symbol)
            if not stock:
                raise ValueError(f"Stock {stock_symbol} not found in the market")
            self.trades.append(Trade(stock=stock, quantity=quantity, type=trade_type, traded_price=price))
            logging.info(f"Recorded trade for {stock_symbol}: {quantity} @ {price}")
        except ValueError as e:
            logging.error(f"ValueError in StockMarket.record_trade: {e}")
            raise
        except Exception as e:
            logging.error(f"Unexpected error in StockMarket.record_trade: {e}")
            raise

    def calculate_volume_weighted_stock_price(self, stock_symbol: str) -> float:
        """
        Calculates the volume weighted stock price for a given stock symbol.

        Args:
            stock_symbol (str): The symbol of the stock for which to calculate the volume weighted stock price.

        Returns:
            float: The volume weighted stock price.
        """
        try:
            now = datetime.now(timezone.utc)
            time_15_minutes_ago = now - timedelta(minutes=15)
            relevant_trades = (trade for trade in self.trades if trade.stock.symbol == stock_symbol and trade.timestamp > time_15_minutes_ago)
            total_product, total_quantity = 0, 0
            for trade in relevant_trades:
                total_product += trade.traded_price * trade.quantity
                total_quantity += trade.quantity
            vwsp = total_product / total_quantity if total_quantity else 0
            logging.info(f"Volume Weighted Stock Price for {stock_symbol}: {vwsp:.2f}")
            return vwsp
        except Exception as e:
            logging.error(f"Unexpected error in StockMarket.calculate_volume_weighted_stock_price: {e}")
            return 0

    def calculate_gbce_all_share_index(self) -> float:
        """
        Calculates the GBCE All Share Index.

        Returns:
            float: The GBCE All Share Index.
        """
        try:
            if not self.trades:
                return 0
            log_sum = sum(log(trade.traded_price) * trade.quantity for trade in self.trades)
            total_quantity = sum(trade.quantity for trade in self.trades)
            gbce_index = exp(log_sum / total_quantity) if total_quantity else 0
            logging.info(f"GBCE All Share Index: {gbce_index:.2f}")
            return gbce_index
        except Exception as e:
            logging.error(f"Unexpected error in StockMarket.calculate_gbce_all_share_index: {e}")
            return 0

    def get_stocks(self, stock_data: List[Dict[str, Union[str, int, float]]]) -> None:
        """
        Get the stock market with stock data.

        Args:
            stock_data (List[Dict[str, Union[str, int, float]]]): A list of dictionaries containing stock data.

        Raises:
            ValueError: If the stock type is unknown or missing.

        Returns:
            None
        """
        try:
            for data in stock_data:
                stock_type = StockType[data['type'].upper()] if isinstance(data.get('type'), str) and data['type'].upper() in StockType.__members__ else None
                if not stock_type:
                    raise ValueError(f"Unknown or missing stock type {data.get('type')}")
                if stock_type == StockType.COMMON:
                    self.stocks[data['symbol']] = CommonStock(symbol=data['symbol'],
                                                              last_dividend=data['last_dividend'],
                                                              par_value=data['par_value'])
                elif stock_type == StockType.PREFERRED:
                    self.stocks[data['symbol']] = PreferredStock(symbol=data['symbol'],
                                                                 last_dividend=data['last_dividend'],
                                                                 par_value=data['par_value'],
                                                                 fixed_dividend=data['fixed_dividend'])
                logging.info(f"Hydrated stock: {data['symbol']}")
        except ValueError as e:
            logging.error(f"ValueError in StockMarket.hydrate_stocks: {e}")
            raise
        except Exception as e:
            logging.error(f"Unexpected error in StockMarket.hydrate_stocks: {e}")
            raise

    def get_trade_details(self) -> List[Dict[str, Union[str, int, float]]]:
        """
        Retrieves the details of all trades recorded in the stock market.

        Returns:
            List[Dict[str, Union[str, int, float]]]: A list of dictionaries containing trade details.
        """
        trade_list = []
        for trade in self.trades:
            trade_details = {
                'symbol': trade.stock.symbol,
                'quantity': trade.quantity,
                'type': trade.type.name,
                'traded_price': trade.traded_price,
                'timestamp': trade.timestamp.isoformat()
            }
            trade_list.append(trade_details)
        return trade_list