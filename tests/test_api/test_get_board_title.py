# -*- coding: utf-8 -*-

import unittest
import logging

from openbbs_middleware.api import get_board_title


class TestGetBoardTitle(unittest.TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_get_board_title(self):
        board_id = 'test_board_id'
        params = {}

        err, results = get_board_title.get_board_title(board_id, params)

        assert err is None
