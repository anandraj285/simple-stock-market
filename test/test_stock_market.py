import unittest
from unittest.mock import patch
from datetime import datetime, timedelta, timezone
from stock_market import StockMarket
from models.stock import CommonStock, PreferredStock
from models.trade import Trade
from models.common import TradeType

class TestStockMarket(unittest.TestCase):

    def setUp(self):
        # Initialize StockMarket instance for each test
        self.market = StockMarket()

    def test_common_stock_dividend_yield(self):
        # Test CommonStock dividend yield calculation
        common_stock = CommonStock(symbol="ABC", last_dividend=8, par_value=100)
        self.assertAlmostEqual(common_stock.calculate_dividend_yield(100), 8.0 / 100)

        # Test handling of zero market price
        with self.assertRaises(ValueError):
            common_stock.calculate_dividend_yield(0)

    def test_preferred_stock_dividend_yield(self):
        # Test PreferredStock dividend yield calculation
        preferred_stock = PreferredStock(symbol="XYZ", last_dividend=8, par_value=100, fixed_dividend=0.02)
        self.assertAlmostEqual(preferred_stock.calculate_dividend_yield(100), (0.02 * 100) / 100)

        # Test handling of zero market price or missing fixed dividend
        with self.assertRaises(ValueError):
            preferred_stock.calculate_dividend_yield(0)

    def test_trade_initialization(self):
        # Test Trade initialization
        common_stock = CommonStock(symbol="ABC", last_dividend=8, par_value=100)
        trade = Trade(stock=common_stock, quantity=100, type=TradeType.BUY, traded_price=100)
        self.assertEqual(trade.stock.symbol, "ABC")
        self.assertEqual(trade.quantity, 100)
        self.assertEqual(trade.type, TradeType.BUY)
        self.assertEqual(trade.traded_price, 100)

        # Test handling of non-positive quantity
        with self.assertRaises(ValueError):
            Trade(stock=common_stock, quantity=-100, type=TradeType.SELL, traded_price=100)

    def test_hydrate_stocks(self):
        # Test hydrating stocks with valid and invalid data
        stock_data = [
            {"symbol": "ABC", "type": "common", "last_dividend": 8, "par_value": 100},
            {"symbol": "XYZ", "type": "preferred", "last_dividend": 8, "fixed_dividend": 0.02, "par_value": 100}
        ]
        self.market.hydrate_stocks(stock_data)
        self.assertEqual(len(self.market.stocks), 2)

        # Test handling of invalid stock data
        invalid_stock_data = [
            {"symbol": "DEF", "type": "unknown", "last_dividend": 10, "par_value": 50}
        ]
        with self.assertRaises(ValueError):
            self.market.hydrate_stocks(invalid_stock_data)

    def test_record_trade(self):
        # Test recording trades
        common_stock = CommonStock(symbol="ABC", last_dividend=8, par_value=100)
        self.market.stocks["ABC"] = common_stock
        self.market.record_trade(stock_symbol="ABC", quantity=100, trade_type=TradeType.BUY, price=100)
        self.assertEqual(len(self.market.trades), 1)

        # Test handling of invalid stock symbol
        with self.assertRaises(ValueError):
            self.market.record_trade(stock_symbol="DEF", quantity=100, trade_type=TradeType.BUY, price=100)

    def test_calculate_volume_weighted_stock_price(self):
        # Test calculating volume weighted stock price
        common_stock = CommonStock(symbol="ABC", last_dividend=8, par_value=100)
        self.market.stocks["ABC"] = common_stock
        self.market.record_trade(stock_symbol="ABC", quantity=100, trade_type=TradeType.BUY, price=100)
        self.market.record_trade(stock_symbol="ABC", quantity=100, trade_type=TradeType.SELL, price=105)
        self.assertAlmostEqual(self.market.calculate_volume_weighted_stock_price("ABC"), 102.5)

    def test_calculate_gbce_all_share_index(self):
        # Test calculating GBCE All Share Index
        common_stock = CommonStock(symbol="ABC", last_dividend=8, par_value=100)
        preferred_stock = PreferredStock(symbol="XYZ", last_dividend=8, par_value=100, fixed_dividend=0.02)
        self.market.stocks["ABC"] = common_stock
        self.market.stocks["XYZ"] = preferred_stock
        self.market.record_trade(stock_symbol="ABC", quantity=100, trade_type=TradeType.BUY, price=100)
        self.market.record_trade(stock_symbol="XYZ", quantity=100, trade_type=TradeType.SELL, price=105)
        self.assertAlmostEqual(self.market.calculate_gbce_all_share_index(), 102.46950765959595)

    def test_pe_ratio_normal_case(self):
        # Test P/E Ratio calculation with mock stock and calculate_dividend_yield
        with patch.object(CommonStock, 'calculate_dividend_yield', return_value=0.05):
            common_stock = CommonStock(symbol="ABC", last_dividend=8, par_value=100)
            pe_ratio = common_stock.calculate_pe_ratio(100)
            self.assertAlmostEqual(pe_ratio, 100 / 0.05)

    def test_pe_ratio_divide_by_zero(self):
        # Test P/E Ratio calculation with mock stock and calculate_dividend_yield returning 0
        with patch.object(CommonStock, 'calculate_dividend_yield', return_value=0):
            common_stock = CommonStock(symbol="ABC", last_dividend=8, par_value=100)
            pe_ratio = common_stock.calculate_pe_ratio(100)
            self.assertEqual(pe_ratio, 0)

    def test_pe_ratio_exception_handling(self):
        # Test P/E Ratio calculation with mock stock and calculate_dividend_yield raising an exception
        with patch.object(CommonStock, 'calculate_dividend_yield', side_effect=ValueError("Test error")):
            common_stock = CommonStock(symbol="ABC", last_dividend=8, par_value=100)
            with patch('logging.error') as mock_logging:
                pe_ratio = common_stock.calculate_pe_ratio(100)
                self.assertEqual(pe_ratio, 0)
                mock_logging.assert_called_once()

    def test_volume_weighted_stock_price_no_trades(self):
        # Test calculating volume weighted stock price with no trades
        common_stock = CommonStock(symbol="ABC", last_dividend=8, par_value=100)
        self.market.stocks["ABC"] = common_stock
        self.assertAlmostEqual(self.market.calculate_volume_weighted_stock_price("ABC"), 0)

    def test_gbce_all_share_index_no_trades(self):
        # Test calculating GBCE All Share Index with no trades
        self.assertAlmostEqual(self.market.calculate_gbce_all_share_index(), 0)

    def test_trade_post_init_positive_traded_price(self):
        # Test Trade __post_init__ with positive traded price
        with patch('logging.error') as mock_logging:
            trade = Trade(stock=CommonStock(symbol="ABC", last_dividend=8, par_value=100), quantity=100, type=TradeType.BUY, traded_price=100)
            self.assertEqual(trade.traded_price, 100)
            mock_logging.assert_not_called()

    def test_trade_post_init_zero_traded_price(self):
        # Test Trade __post_init__ with zero traded price
        with patch('logging.error') as mock_logging:
            with self.assertRaises(ValueError):
                Trade(stock=CommonStock(symbol="ABC", last_dividend=8, par_value=100), quantity=100, type=TradeType.BUY, traded_price=0)
            mock_logging.assert_called_once()

    def test_trade_post_init_negative_traded_price(self):
        # Test Trade __post_init__ with negative traded price
        with patch('logging.error') as mock_logging:
            with self.assertRaises(ValueError):
                Trade(stock=CommonStock(symbol="ABC", last_dividend=8, par_value=100), quantity=100, type=TradeType.BUY, traded_price=-100)
            mock_logging.assert_called_once()


if __name__ == "__main__":
    unittest.main()

