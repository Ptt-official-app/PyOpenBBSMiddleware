# -*- coding: utf-8 -*-

import unittest
import logging

from openbbs_middleware.api import get_board_category_list


class TestGetBoardCategoryList(unittest.TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_get_board_category_list(self):

        params = {}

        err, results = get_board_category_list.get_board_category_list(params)

        assert err is None
