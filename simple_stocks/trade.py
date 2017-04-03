class Trade(object):
    """Represents a single trade."""

    timestamp = 0
    symbol = ""
    quantity = 0
    trade_type = ""
    price = 0.0

    def __init__(self, *initial_data, **kwargs):
        for dictionary in initial_data:
            for key in dictionary:
                setattr(self, key, dictionary[key])
        for key in kwargs:
            setattr(self, key, kwargs[key])

    def __repr__(self):
        return "%s@%f" % (self.symbol, self.timestamp)
