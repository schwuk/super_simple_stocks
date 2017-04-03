from datetime import datetime
from functools import reduce

from .constants import STOCK_TYPES, TRADE_TYPES
from .stock import Stock


def get_stock(stocks, symbol):
    """Retrieve a stock from a list."""
    stock = list(filter(lambda x: x.symbol == symbol, stocks))
    if len(stock) == 0:
        return None

    return stock[0]


def add_stock(stocks, stock):
    """Add a new stock to a list, returning a copy of the list."""
    _stocks = stocks[:]
    # Validate stocks
    if not isinstance(stock, Stock):
        raise TypeError('stock must be a Stock')

    # Validate symbol
    if get_stock(_stocks, stock.symbol):
        raise ValueError('Stock already exists')

    # Validate type
    if stock.stock_type.title() not in STOCK_TYPES:
        raise ValueError('Invalid stock type; must be in: %s' %
                         (", ".join(STOCK_TYPES)))

    # Add stock
    _stocks.append(stock)

    return _stocks


def record_trade(trades, stock, trade):
    """Add a new trade to a list, returning a copy of the list."""
    _trades = trades[:]

    # Validate type
    if trade.trade_type not in TRADE_TYPES:
        raise ValueError('Invalid trade type; must be in: %s' %
                         (", ".join(TRADE_TYPES)))

    # Record trade
    trade.timestamp = datetime.utcnow().timestamp()
    _trades.append(trade)

    # Update ticker_price
    stock.ticker_price = trade.price

    return _trades


def all_share_index(stocks, trades):
    _product = 0.0

    _prices = map(lambda x: x.get_stock_price(trades), stocks)
    _product = reduce(lambda x, y: x * y, _prices)

    return round(_product ** (1.0 / len(stocks)), 2)
