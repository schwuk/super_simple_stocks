"""Sample data for testing."""

from .stock import Stock


TEA = Stock({'symbol': 'TEA', 'stock_type': 'Common', 'last_dividend': 0,
             'fixed_dividend': None, 'par_value': 100, 'ticker_price': 0})
POP = Stock({'symbol': 'POP', 'stock_type': 'Common', 'last_dividend': 8,
             'fixed_dividend': None, 'par_value': 100, 'ticker_price': 0})
ALE = Stock({'symbol': 'ALE', 'stock_type': 'Common', 'last_dividend': 23,
             'fixed_dividend': None, 'par_value': 60, 'ticker_price': 0})
GIN = Stock({'symbol': 'GIN', 'stock_type': 'Preferred', 'last_dividend': 8,
             'fixed_dividend': 2, 'par_value': 100, 'ticker_price': 0})
JOE = Stock({'symbol': 'JOE', 'stock_type': 'Common', 'last_dividend': 13,
             'fixed_dividend': None, 'par_value': 250, 'ticker_price': 0})
