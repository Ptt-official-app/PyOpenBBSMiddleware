# -*- coding: utf-8 -*-

import unittest
import logging

from openbbs_middleware.api import sort_comment_by_rating


class TestSortCommentByRating(unittest.TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_sort_comment_by_rating(self):
        params = {}

        err, results = sort_comment_by_rating.sort_comment_by_rating(params)

        assert err is None
