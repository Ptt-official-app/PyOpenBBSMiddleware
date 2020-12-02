# -*- coding: utf-8 -*-

import unittest
import logging

from openbbs_middleware.api import get_popular_board_list


class TestGetPopularBoardList(unittest.TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_get_popular_board_list(self):
        params = {}

        err, results = get_popular_board_list.get_popular_board_list(params)

        assert err is None
