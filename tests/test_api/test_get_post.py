# -*- coding: utf-8 -*-

import unittest
import logging

from openbbs_middleware.api import get_post


class TestGetPost(unittest.TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_get_post(self):
        board_id = 'test_board_id'
        user_id = 'test_user_id'
        params = {}

        err, results = get_post.get_post(board_id, user_id, params)

        assert err is None
