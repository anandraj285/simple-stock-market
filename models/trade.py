from models.stock import Stock
from dataclasses import dataclass, field
from models.common import TradeType
from datetime import datetime, timezone
import logging

@dataclass
class Trade:
    """
    Represents a trade in the stock market.

    Attributes:
        stock (Stock): The stock being traded.
        quantity (int): The quantity of stocks being traded.
        type (TradeType): The type of trade (buy or sell).
        traded_price (float): The price at which the trade was executed.
        timestamp (datetime): The timestamp of the trade (default is the current UTC time).
    """

    stock: Stock
    quantity: int
    type: TradeType
    traded_price: float
    timestamp: datetime = field(default_factory=lambda: datetime.now(timezone.utc))

    def __post_init__(self):
        """
        Performs post-initialization validation for the Trade object.

        Raises:
            ValueError: If the quantity or traded_price is less than or equal to zero.
        """
        try:
            if self.quantity <= 0:
                raise ValueError("Trade quantity must be greater than zero")
            if self.traded_price <= 0:
                raise ValueError("Traded price must be greater than zero")
        except ValueError as e:
            logging.error(f"ValueError in Trade.__post_init__: {e}")
            raise
        except Exception as e:
            logging.error(f"Unexpected error in Trade.__post_init__: {e}")
            raise