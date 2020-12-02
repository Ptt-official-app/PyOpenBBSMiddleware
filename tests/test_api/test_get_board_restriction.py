# -*- coding: utf-8 -*-

import unittest
import logging

from openbbs_middleware.api import get_board_restriction


class TestGetBoardRestriction(unittest.TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_get_board_restriction(self):
        params = {}

        err, results = get_board_restriction.get_board_restriction(params)

        assert err is None
