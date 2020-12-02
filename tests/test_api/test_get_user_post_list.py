# -*- coding: utf-8 -*-

import unittest
import logging

from openbbs_middleware.api import get_user_post_list


class TestGetUserPostList(unittest.TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_get_user_post_list(self):
        user_id = 'test_user_id'
        params = {}

        err, results = get_user_post_list.get_user_post_list(user_id, params)

        assert err is None
