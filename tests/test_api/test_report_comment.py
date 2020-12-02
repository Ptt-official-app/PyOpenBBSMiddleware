# -*- coding: utf-8 -*-

import unittest
import logging

from openbbs_middleware.api import report_comment


class TestReportComment(unittest.TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_report_comment(self):
        params = {}

        err, results = report_comment.report_comment(params)

        assert err is None
