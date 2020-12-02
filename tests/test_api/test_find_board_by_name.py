# -*- coding: utf-8 -*-

import unittest
import logging

from openbbs_middleware.api import find_board_by_name


class TestFindBoardByName(unittest.TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_find_board_by_name(self):
        params = {
        }

        err, result = find_board_by_name.find_board_by_name(params)

        assert err is None
