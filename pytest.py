#pytest

import unittest
import numpy as np
import pandas as pd
from unittest.mock import MagicMock
from function_principal import *
from datetime import datetime
from functions_support import *

class TestBotFunctions(unittest.TestCase):

    def test_on_open(self):
        # Mocking WebSocket connection object
        ws_mock = MagicMock()

        # Test if on_open function executes without raising an exception
        try:
            on_open(ws_mock)
        except Exception as e:
            self.fail(f"on_open function raised an unexpected exception: {e}")

    def test_on_close(self):
        # Mocking WebSocket connection object
        ws_mock = MagicMock()

        # Test if on_close function executes without raising an exception
        try:
            on_close(ws_mock)
        except Exception as e:
            self.fail(f"on_close function raised an unexpected exception: {e}")

    def test_on_message(self):
        # Mocking WebSocket connection object and message
        ws_mock = MagicMock()
        message = '{"k": {"c": "100", "x": true}}'  # Example message JSON string

        # Test if on_message function executes without raising an exception
        try:
            on_message(ws_mock, message)
        except Exception as e:
            self.fail(f"on_message function raised an unexpected exception: {e}")

        # You may add more specific tests here to check the printed output, if necessary

class TestBotFunctions(unittest.TestCase):

    def test_interval_offset(self):
        # Test interval_offset function with different intervals
        self.assertEqual(interval_offset('1m'), pd.DateOffset(minutes=1))
        self.assertEqual(interval_offset('5m'), pd.DateOffset(minutes=5))
        self.assertEqual(interval_offset('1h'), pd.DateOffset(hours=1))
        # Add more test cases as needed

    def test_calculates_ema(self):
        # Test with known inputs and expected output
        close = 50
        period = 10
        smoothing = 2
        ema_list = [45, 48, 52, 49, 53, 51, 50, 55, 57, 60]  # Example list of previous EMA values
        expected_ema = 52.05263157894737  # Expected EMA value for the given inputs

        # Call the function with the test inputs
        actual_ema = calculates_ema(close, period, smoothing, ema_list)

        # Assert that the actual result matches the expected result
        self.assertAlmostEqual(actual_ema, expected_ema, places=10)

    def test_ret_ema(self):
        # Test ret_ema function
        prev_closes = [10, 20, 30, 40, 50]
        self.assertAlmostEqual(ret_ema(prev_closes, 5), 44.0)
        # Add more test cases as needed

    def test_time_select(self):
        # Test time_select function
        ema10 = 10
        ema20 = 20
        self.assertEqual(time_select('1m', ema10, ema20), (datetime.now().strftime("%m-%d-%Y %H:%M"), datetime.now().strftime("%m-%d-%Y %H:%M")))
        # Add more test cases as needed

    # Add more test functions for other functions as needed

if __name__ == '__main__':
    unittest.main()
