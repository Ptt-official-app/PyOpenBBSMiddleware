# -*- coding: utf-8 -*-

import unittest
import logging

from openbbs_middleware.api import report_post


class TestReportPost(unittest.TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_report_post(self):
        params = {}

        err, results = report_post.report_post(params)

        assert err is None
