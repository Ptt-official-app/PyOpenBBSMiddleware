# -*- coding: utf-8 -*-

import unittest
import logging

from openbbs_middleware.api import report_author


class TestReportAuthor(unittest.TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_report_author(self):
        params = {}

        err, results = report_author.report_author(params)

        assert err is None
