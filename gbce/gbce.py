from cmd import Cmd

from tabulate import tabulate

from simple_stocks import add_stock, all_share_index, get_stock, record_trade,\
                          Stock, Trade
from simple_stocks.constants import BUY, COMMON, PREFERRED, SELL
from simple_stocks.sample_data import TEA, POP, ALE, GIN, JOE


def get_symbol_input(symbol=""):
    message = "Stock symbol (three letters): "
    regex = r'^[A-Za-z]{3}$'
    return get_valid_text_input(message, regex, symbol).upper()


def get_valid_text_input(message, regex, text=""):
    while len(text) == 0:
        text = input(message)
        import re
        if not re.search(regex, text):
            text = ""
    return text


def get_choice_input(message, valid_choices):
    choice = -1
    while choice not in valid_choices:
        try:
            choice = int(input(message))
        except ValueError:
            choice = -1
    return choice


def get_float_input(message):
    value = -1.0
    while value < 0:
        try:
            value = float(input(message))
        except ValueError:
            value = -1.0
    return value


class GBCE(Cmd):

    stocks = []
    trades = []

    def do_seed_stocks(self, args):
        """Populate with sample stocks."""
        for stock in (TEA, POP, ALE, GIN, JOE):
            try:
                _stocks = add_stock(self.stocks, stock)
                if len(_stocks) > len(self.stocks):
                    self.stocks = _stocks
                    print("Added %s to the list of stocks" % stock)
            except ValueError as e:
                print("Unable to add %s: %s" % (stock, str(e)))

    def do_stocks(self, args):
        """List all stocks."""
        _stocks = []
        for stock in self.stocks:
            _stock = stock.__dict__
            _stock['stock_price'] = stock.get_stock_price(self.trades)
            _stock['yield'] = stock.get_dividend_yield()
            _stock['pe_ratio'] = stock.get_pe_ratio()
            _stocks.append(_stock)
        print(tabulate(_stocks, headers="keys"))

    def do_stock(self, symbol):
        """List a single stock. E.g., stock TEA"""
        stock = get_stock(self.stocks, symbol)
        if stock:
            print(tabulate([stock.__dict__], headers="keys"))
        else:
            print("Stock %s not found" % symbol)

    def do_add_stock(self, symbol):
        """
        Add a new stock.

        You will be prompted for the stock details.
        """
        stock = Stock()

        # symbol
        stock.symbol = get_symbol_input(symbol)

        # stock_type
        stock_type = get_choice_input("'1' for Common, '2' for Preferred: ",
                                      (1, 2))
        if stock_type == 2:
            stock.stock_type = PREFERRED
        else:
            stock.stock_type = COMMON

        # last_dividend
        stock.last_dividend = get_float_input("Last Dividend: ")

        # fixed_dividend
        if stock.stock_type == COMMON:
            stock.fixed_dividend = None
        else:
            stock.fixed_dividend = get_float_input("Fixed Dividend: ")

        # par_value
        stock.par_value = get_float_input("Par Value: ")
        stock.ticker_price = 0.0

        try:
            self.stocks = add_stock(self.stocks, stock)
            print("Stock %s added!" % stock)
        except ValueError as e:
            print("Unable to add %s: %s" % (stock, str(e)))

    def do_record_trade(self, symbol):
        """
        Record a trade for a given stock.

        You will be prompted for the trade details.
        """
        symbol = get_symbol_input(symbol)
        stock = get_stock(self.stocks, symbol)
        if not stock:
            print("Stock %s not found" % symbol)
            return

        trade = Trade()
        trade.symbol = symbol

        trade_type = get_choice_input("'1' for BUY, '2' for SELL: ",
                                      (1, 2))
        if trade_type == 1:
            trade.trade_type = BUY
        else:
            trade.trade_type = SELL

        trade.quantity = get_float_input("Quantity: ")

        trade.price = get_float_input("Price: ")

        try:
            self.trades = record_trade(self.trades, stock, trade)
            print("Trade %s added!" % trade)
        except ValueError as e:
            print("Unable to add %s: %s" % (trade, str(e)))

    def do_all_share_index(self, args):
        """Calculate the all share index."""
        print(all_share_index(self.stocks, self.trades))

    def do_quit(self, args):
        """Quit the program."""
        print("Quitting.")
        raise SystemExit
