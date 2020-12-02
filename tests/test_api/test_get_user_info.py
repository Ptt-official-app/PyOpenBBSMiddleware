# -*- coding: utf-8 -*-

import unittest
import logging

from openbbs_middleware.api import get_user_info


class TestGetUserInfo(unittest.TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_get_user_info(self):
        user_id = 'test_user_id'
        params = {}

        err, results = get_user_info.get_user_info(user_id, params)

        assert err is None
