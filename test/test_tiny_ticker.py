import unittest
from unittest.mock import patch
from controller.tiny_ticker import main, ticker_argument_parser
from view.main_view import MainView
import tkinter as tk
import os
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

class TestStart(unittest.TestCase):

    @patch('controller.tiny_ticker.ticker_argument_parser')
    @patch('controller.tiny_ticker.parse')
    def test_call_ticker_argument_parser(self, mock_arg_parser, mock_parser):
        """ Unit test for controller.tiny_ticker.main. Tests the call to the argument parser"""

        root = tk.Tk()
        test_view = MainView(master=root)
        main(test_view)
        mock_arg_parser.assert_called()

    @patch('controller.tiny_ticker.parse')
    def test_call_parse(self, mock_parser):
        """ Unit test for controller.tiny_ticker.main. Tests the call to the model's feedmanager.parse """
        fake_url = ['www.fakeurl.com']
        sys.argv = ['test', '--url', fake_url[0]]
        root = tk.Tk()
        test_view = MainView(master=root)
        main(test_view)
        mock_parser.assert_called_with(fake_url[0])

    @patch('controller.tiny_ticker.ten_second_loop')
    @patch('controller.tiny_ticker.parse')
    def test_call_ten_second_loop(self, mock_loop, mock_parser):
        """ Unit test for controller.tiny_ticker.main. Tests the call to the ten second loop """

        root = tk.Tk()
        test_view = MainView(master=root)
        main(test_view)
        mock_loop.assert_called_with('www.fakeurl.com',)

