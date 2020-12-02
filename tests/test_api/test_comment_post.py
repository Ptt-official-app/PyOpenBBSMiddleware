# -*- coding: utf-8 -*-

import unittest
import logging

from openbbs_middleware.api import comment_post


class TestCommentPost(unittest.TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_comment_post(self):
        params = {
        }

        err, result = comment_post.comment_post(params)

        assert err is None
