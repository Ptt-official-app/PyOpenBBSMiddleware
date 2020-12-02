# -*- coding: utf-8 -*-

import unittest
import logging

from openbbs_middleware.api import forward_post_to_board


class TestForwardPostToBoard(unittest.TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_forward_post_to_board(self):
        params = {}

        err, results = forward_post_to_board.forward_post_to_board(params)

        assert err is None
