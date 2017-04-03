"""Tests for simple_stocks."""
import unittest

from copy import copy

from .sample_data import TEA, POP
from .simple_stocks import add_stock, all_share_index, get_stock, record_trade
from .trade import Trade


class TestGetStock(unittest.TestCase):
    """Tests for the `get_stock` function."""

    def test_no_stocks(self):
        """If the stock cannot be found, the result will be `False`."""
        stocks = []
        symbol = 'TEA'
        self.assertIsNone(get_stock(stocks, symbol))

    def test_default(self):
        """Default behaviour."""
        stocks = [TEA, ]
        self.assertEqual(get_stock(stocks, TEA.symbol), TEA)

    def test_duplicate_stocks(self):
        """
        Ensure we get the first stock when there are duplicates.

        This should never happen as `add_stock` will not allow you to create
        duplicate symbols.
        """
        stocks = [TEA, ]
        new_stock = copy(TEA)
        new_stock.last_dividend = 10
        stocks = [TEA, new_stock]
        self.assertEqual(get_stock(stocks, TEA.symbol), TEA)


class TestAddStock(unittest.TestCase):
    """Tests for the `add_stock` function."""

    def test_default(self):
        """The default behaviour is to return a copy of the list."""
        stocks = [TEA, ]
        result = add_stock(stocks, POP)
        self.assertEqual(2, len(result))
        self.assertEqual(1, len(stocks))

    def test_args(self):
        """`add_stock` requires you pass in a `Stock` object."""
        self.assertRaises(TypeError, add_stock, [], {})

    def test_stock_already_exists(self):
        stocks = [TEA, ]
        self.assertRaises(ValueError, add_stock, stocks, TEA)

    def test_stock_type(self):
        stocks = [TEA, ]
        new_stock = copy(TEA)
        new_stock.symbol = 'FOO'
        new_stock.stock_type = 'Apples'
        self.assertRaises(ValueError, add_stock, stocks, new_stock)
        new_stock.stock_type = 'Common'
        result = add_stock(stocks, new_stock)
        self.assertEqual(2, len(result))
        self.assertEqual(1, len(stocks))
        new_stock.symbol = 'BAR'
        new_stock.stock_type = 'Preferred'
        result = add_stock(stocks, new_stock)
        self.assertEqual(2, len(result))
        self.assertEqual(1, len(stocks))


class TestRecordTrade(unittest.TestCase):
    """Tests for the `record_trade` function."""

    def test_default(self):
        trades = []
        trade = Trade()
        trade.symbol = TEA.symbol
        trade.quantity = 1
        trade.trade_type = 'BUY'
        trade.price = 10
        result = record_trade(trades, TEA, trade)
        self.assertEqual(1, len(result))
        self.assertEqual(0, len(trades))
        self.assertEqual(trade, result[0])

    def test_trade_type(self):
        trades = []
        trade = Trade()
        trade.symbol = TEA.symbol
        trade.quantity = 1
        trade.trade_type = 'FOO'
        trade.price = 10
        self.assertRaises(ValueError, record_trade, trades, TEA, trade)
        trade.trade_type = 'BUY'
        result = record_trade(trades, TEA, trade)
        self.assertEqual(1, len(result))
        self.assertEqual(0, len(trades))
        self.assertEqual(trade, result[0])
        trades = result
        trade.trade_type = 'SELL'
        result = record_trade(trades, TEA, trade)
        self.assertEqual(2, len(result))
        self.assertEqual(1, len(trades))
        self.assertEqual(trade, result[1])


class TestAllShareIndex(unittest.TestCase):
    """Tests for the `all_share_index` function."""

    def test_default(self):
        expected_index = 1.41

        stocks = [TEA, POP]
        trades = []

        trade = Trade()
        trade.symbol = TEA.symbol
        trade.quantity = 1
        trade.trade_type = 'BUY'
        trade.price = 1
        trades = record_trade(trades, TEA, trade)

        trade = Trade()
        trade.symbol = POP.symbol
        trade.quantity = 1
        trade.trade_type = 'BUY'
        trade.price = 2
        trades = record_trade(trades, POP, trade)

        self.assertEqual(all_share_index(stocks, trades), expected_index)


if __name__ == '__main__':
    unittest.main()
