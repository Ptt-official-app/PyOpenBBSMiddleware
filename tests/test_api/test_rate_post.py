# -*- coding: utf-8 -*-

import unittest
import logging

from openbbs_middleware.api import rate_post


class TestRatePost(unittest.TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_rate_post(self):

        params = {}
        err, results = rate_post.rate_post(params)

        assert err is None
