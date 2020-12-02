# -*- coding: utf-8 -*-

import unittest
import logging

from openbbs_middleware.api import get_app_info


class TestGetAppInfo(unittest.TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_get_app_info(self):
        params = {}

        err, results = get_app_info.get_app_info(params)

        assert err is None
