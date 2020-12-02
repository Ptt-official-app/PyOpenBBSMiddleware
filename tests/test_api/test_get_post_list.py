# -*- coding: utf-8 -*-

import unittest
import logging

from openbbs_middleware.api import get_post_list


class TestGetPostList(unittest.TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_get_post_list(self):
        bid = 'test_bid'
        params = {}

        err, results = get_post_list.get_post_list(bid, params)

        assert err is None
