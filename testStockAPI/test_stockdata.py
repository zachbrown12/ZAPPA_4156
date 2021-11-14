import unittest
from stockdata import Stockdata


class Test_TestStockdata(unittest.TestCase):

    # Tests that a valid ticker returns acceptable values
    def test_good_ticker(self):
        s = Stockdata("AAPL")
        self.assertTrue(type(s.ask_price()) is float)
        self.assertTrue(type(s.bid_price()) is float)

    # Tests that a ticker that doesn't exist raises an error
    def test_bad_ticker(self):
        s = Stockdata("ZAPPA")
        self.assertIsNone(s.ask_price())
        self.assertIsNone(s.bid_price())

    # Tests that a garbled/invalid ticker raises an error
    def test_invalid_ticker(self):
        s = Stockdata("^#12*")
        self.assertIsNone(s.ask_price())
        self.assertIsNone(s.bid_price())

    # Tests that a non-string ticker raises an error
    def test_number_ticker(self):
        s = Stockdata(123)
        self.assertIsNone(s.ask_price())
        self.assertIsNone(s.bid_price())

    # Tests that a None ticker raises an error
    def test_none_ticker(self):
        s = Stockdata(None)
        self.assertIsNone(s.ask_price())
        self.assertIsNone(s.bid_price())
