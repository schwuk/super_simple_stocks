"""Stock model."""

from datetime import datetime, timedelta

from .constants import PREFERRED


class Stock(object):
    """Represents a single stock."""

    symbol = ""
    stock_type = ""
    last_dividend = 0
    fixed_dividend = 0
    par_value = 0
    ticker_price = 0.0

    def __init__(self, *initial_data, **kwargs):
        """Create a new Stock."""
        for dictionary in initial_data:
            for key in dictionary:
                setattr(self, key, dictionary[key])
        for key in kwargs:
            setattr(self, key, kwargs[key])

    def __repr__(self):
        return self.symbol

    def get_stock_price(self, trades):
        """
        Get the price for this stock.

        Calculated from trades within the last fifteen minutes.
        """
        cutoff = (datetime.utcnow() - timedelta(minutes=15)).timestamp()

        _trades = list(filter(lambda x: x.timestamp >= cutoff and
                              x.symbol == self.symbol, trades))

        sum_price = 0.0
        sum_quantity = 0.0
        for trade in _trades:
            sum_price += trade.price * trade.quantity
            sum_quantity += trade.quantity

        try:
            price = sum_price / sum_quantity
        except ZeroDivisionError:
            price = 0.0

        return price

    def get_dividend_yield(self):
        """Get the dividend yield for this stock."""
        try:
            if self.stock_type == PREFERRED:
                _yield = ((self.fixed_dividend / 100) * self.par_value) /\
                    self.ticker_price
            else:
                _yield = self.last_dividend / self.ticker_price
        except ZeroDivisionError:
            _yield = 0.0

        return _yield

    def get_pe_ratio(self):
        """Get the price/earnings ratio for this stock."""
        try:
            _ratio = self.ticker_price / self.get_dividend_yield()
        except ZeroDivisionError:
            _ratio = 0.0

        return _ratio
