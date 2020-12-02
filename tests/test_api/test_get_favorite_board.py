# -*- coding: utf-8 -*-

import unittest
import logging

from openbbs_middleware.api import get_favorite_board


class TestGetFavoriteBoard(unittest.TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_get_favorite_board(self):
        user_id = 'test_user_id'
        params = {}
        err, results = get_favorite_board.get_favorite_board(user_id, params)

        assert err is None
