# -*- coding: utf-8 -*-

import unittest
import logging

from openbbs_middleware.api import rate_comment


class TestRateComment(unittest.TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_rate_comment(self):
        params = {}

        err, results = rate_comment.rate_comment(params)

        assert err is None
