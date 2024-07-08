from enum import Enum, auto

class StockType(Enum):
    """
    Enumeration representing the type of stock.
    
    Attributes:
        COMMON: Represents a common stock.
        PREFERRED: Represents a preferred stock.
    """
    COMMON = auto()
    PREFERRED = auto()



class TradeType(Enum):
    """
    Enum representing the type of trade.

    Attributes:
        BUY: Represents a buy trade.
        SELL: Represents a sell trade.
    """
    BUY = auto()
    SELL = auto()
