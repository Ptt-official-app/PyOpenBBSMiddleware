# -*- coding: utf-8 -*-

import unittest
import logging

from openbbs_middleware.api import get_board_moderators


class TestGetBoardModerators(unittest.TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_get_board_moderators(self):
        params = {}
        err, results = get_board_moderators.get_board_moderators(params)

        assert err is None
