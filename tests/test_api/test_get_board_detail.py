# -*- coding: utf-8 -*-

import unittest
import logging

from openbbs_middleware.api import get_board_detail


class TestGetBoardDetail(unittest.TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_get_board_detail(self):
        bid = 'test_bid'
        params = {}

        err, results = get_board_detail.get_board_detail(bid, params)

        assert err is None
