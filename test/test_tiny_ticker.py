"""Test.test_tiny_ticker."""
import os
import sys
import unittest
import tkinter as tk
from datetime import datetime
from model.feed import Feed
from model.article import Article
from unittest.mock import patch
from view.main_view import MainView
from model.feed_manager import FeedManager
from controller.tiny_ticker import main, ten_second_loop, call_switch_display


sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

class TestMain(unittest.TestCase):

    """Test class for controller.tiny_ticker."""

    @classmethod
    def setUp(cls):
        """Test.test_tiny_ticker.TestTinyTicker.setUp."""
        root = tk.Tk()
        cls.test_view = MainView(master=root)

    @classmethod
    def tearDown(cls):
        """Test.test_tiny_ticker.TestTinyTicker.tearDown."""
        cls.test_view.destroy()

    @patch('controller.tiny_ticker.ticker_argument_parser')
    def test_call_ticker_argument_parser(self, mock_arg_parser):
        """Unit test for controller.tiny_ticker.main. Tests the call to the argument parser."""
        test_url = 'http://www.fakeurl.com/rss'
        main(self.test_view)
        mock_arg_parser.assert_called()

    @patch('model.parser')
    def test_call_parse(self, mock_parser):
        """Unit test for controller.tiny_ticker.main. Tests the call to the model's feedmanager.parse."""
        test_url = ['http://www.fakeurl.com/rss']
        sys.argv = ['test', '--url', test_url[0]]

        main(self.test_view)
        mock_parser.assert_called_with(test_url[0])

    @patch('controller.tiny_ticker.ten_second_loop')
    def test_call_ten_second_loop(self, mock_loop):
        """Unit test for controller.tiny_ticker.main. Tests the call to the ten second loop."""
        test_url = ['http://www.fakeurl.com/rss']
        main(self.test_view)
        mock_loop.assert_called_with('www.fakeurl.com/rss')


class TestLoop(unittest.TestCase):

    test_title = 'test title'
    test_url = 'www.nowhere.com'
    test_date = '5/11/2020'

    @patch('controller.tiny_ticker.th.Timer')
    @patch('view.main_view')
    @patch('controller.tiny_ticker.call_switch_display')
    def test_ten_second_loop_calls_its_self(self, mock_timer, mock_main_view, mock_switch_display):
        """Unit test of controller.title_loop.ten_second_loop"""

        test_feed_manager = FeedManager()
        test_article = Article(self.test_title, self.test_url, datetime.now())
        test_feed_manager.update("Test Feed Title", "Test Feed Url", [test_article])

        ten_second_loop(mock_main_view, 7, test_feed_manager)
        self.assertTrue(mock_timer.called)
        self.assertTrue(mock_switch_display.called)

    @patch('view.main_view.MainView')
    def test_call_switch_display(self, mock_main_view):
        """Unit test of controller.title_loop.call_switch_display"""

        test_feed_manager = FeedManager()
        test_article = Article(self.test_title, self.test_url, datetime.now())
        test_feed_manager.update("Test Feed Title", "Test Feed Url", [test_article])

        call_switch_display(mock_main_view, test_feed_manager)
        mock_main_view.display_entry.assert_called_with(self.test_title, self.test_url)
