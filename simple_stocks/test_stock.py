"""Tests for the Stock object."""
import unittest

from .sample_data import ALE, GIN
from .simple_stocks import record_trade
from .trade import Trade


class TestStock(unittest.TestCase):

    def test_get_stock_price(self):
        expected_price = 15.0  # (5*1 + 20*2) / 3
        stock = ALE

        trades = []

        trade = Trade()
        trade.symbol = ALE.symbol
        trade.quantity = 1
        trade.trade_type = 'BUY'
        trade.price = 5
        trades = record_trade(trades, stock, trade)
        trade = Trade()
        trade.symbol = ALE.symbol
        trade.trade_type = 'BUY'
        trade.quantity = 2
        trade.price = 20
        trades = record_trade(trades, stock, trade)

        self.assertEqual(expected_price, stock.get_stock_price(trades))

    def test_get_dividend_yield(self):
        expected_yield = 2.3  # 23 / 10
        stock = ALE
        stock.ticker_price = 10
        self.assertEqual(stock.get_dividend_yield(), expected_yield)

    def test_get_dividend_yield_preferred(self):
        expected_yield = 0.2  # ((2/100) * 100) / 10
        stock = GIN
        stock.ticker_price = 10
        self.assertEqual(stock.get_dividend_yield(), expected_yield)

    def test_get_pe_ratio(self):
        expected_ratio = 4.347826086956522  # 10 / 2.3
        stock = ALE
        stock.ticker_price = 10
        self.assertEqual(stock.get_pe_ratio(), expected_ratio)

    def test_get_pe_ratio_preferred(self):
        expected_ratio = 50.0  # 10 / 0.2
        stock = GIN
        stock.ticker_price = 10
        self.assertEqual(stock.get_pe_ratio(), expected_ratio)
