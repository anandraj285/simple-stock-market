import logging
from dataclasses import dataclass
from typing import Optional

@dataclass
class Stock:
    """
    Represents a stock in the stock market.

    Attributes:
    - symbol: The symbol of the stock.
    - last_dividend: The last dividend of the stock. (optional)
    - par_value: The par value of the stock. (optional)
    """

    symbol: str
    last_dividend: Optional[int] = None
    par_value: Optional[int] = None

    def calculate_pe_ratio(self, market_price: float) -> float:
        """
        Calculates the price-to-earnings ratio (PE ratio) for the stock.

        Parameters:
        - market_price: The market price of the stock.

        Returns:
        - The calculated PE ratio.

        If an error occurs during the calculation, it is logged and 0 is returned.
        """
        try:
            if (dividend_yield := self.calculate_dividend_yield(market_price)) == 0:
                return 0
            return market_price / dividend_yield
        except Exception as e:
            logging.error(f"Error calculating PE Ratio for {self.symbol}: {e}")
            return 0

    def calculate_dividend_yield(self, market_price: float) -> float:
        """
        Calculates the dividend yield for the stock.

        Parameters:
        - market_price: The market price of the stock.

        Returns:
        - The calculated dividend yield.

        This method is meant to be implemented in subclasses.
        """
        raise NotImplementedError("Must be implemented in subclasses")
    
@dataclass
class CommonStock(Stock):
    """Represents a common stock in the stock market."""

    def calculate_dividend_yield(self, market_price: float) -> float:
        """
        Calculates the dividend yield for the common stock.

        Args:
            market_price (float): The market price of the stock.

        Returns:
            float: The dividend yield calculated based on the market price and last dividend.

        Raises:
            ValueError: If the market price is less than or equal to zero.
            Exception: If any unexpected error occurs during the calculation.

        """
        try:
            if market_price <= 0:
                raise ValueError("Market price must be greater than zero")
            return self.last_dividend / market_price if self.last_dividend else 0
        except ValueError as e:
            logging.error(f"ValueError in CommonStock.calculate_dividend_yield for {self.symbol}: {e}")
            raise
        except Exception as e:
            logging.error(f"Unexpected error in CommonStock.calculate_dividend_yield for {self.symbol}: {e}")
            raise

@dataclass
class PreferredStock(Stock):
    """
    Represents a preferred stock.

    Attributes:
        fixed_dividend (Optional[float]): The fixed dividend rate of the preferred stock.
    """

    fixed_dividend: Optional[float] = None

    def calculate_dividend_yield(self, market_price: float) -> float:
        """
        Calculates the dividend yield of the preferred stock.

        Args:
            market_price (float): The market price of the stock.

        Returns:
            float: The dividend yield.

        Raises:
            ValueError: If the market price is invalid or the fixed dividend is not set.
        """
        try:
            if market_price <= 0 or not self.fixed_dividend:
                raise ValueError("Invalid market price or fixed dividend")
            return (self.fixed_dividend * self.par_value) / market_price
        except ValueError as e:
            logging.error(f"ValueError in PreferredStock.calculate_dividend_yield for {self.symbol}: {e}")
            raise
        except Exception as e:
            logging.error(f"Unexpected error in PreferredStock.calculate_dividend_yield for {self.symbol}: {e}")
            raise