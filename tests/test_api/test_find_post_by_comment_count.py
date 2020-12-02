# -*- coding: utf-8 -*-

import unittest
import logging

from openbbs_middleware.api import find_post_by_comment_count


class TestFindPostByCommentCount(unittest.TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_find_post_by_comment_count(self):
        params = {
        }

        err, result = find_post_by_comment_count.find_post_by_comment_count(params)

        assert err is None