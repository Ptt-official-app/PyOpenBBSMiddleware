# -*- coding: utf-8 -*-

import unittest
import logging

from openbbs_middleware.api import get_user_setting


class TestGetUserSetting(unittest.TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_get_user_setting(self):
        params = {}

        err, results = get_user_setting.get_user_setting(params)

        assert err is None
