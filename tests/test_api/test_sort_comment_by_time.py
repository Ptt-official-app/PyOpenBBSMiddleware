# -*- coding: utf-8 -*-

import unittest
import logging

from openbbs_middleware.api import sort_comment_by_time


class TestSortCommentByTime(unittest.TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_sort_comment_by_time(self):

        params = {}

        err, results = sort_comment_by_time.sort_comment_by_time(params)

        assert err is None
