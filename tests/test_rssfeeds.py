import sys

sys.path.append('/Users/jamescoleman/PycharmProjects/Python-RSS-ticker/Controller')

import unittest
from rssfeeds import feed as rs

class TestRSSFeed(unittest.TestCase):

    def test_rssFeedDemo(self):
        assert rs.rssFeedDemoModule() == 'inside rss Feed Demo Module'


if __name__ == '__main__':
    unittest.main()
