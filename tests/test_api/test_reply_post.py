# -*- coding: utf-8 -*-

import unittest
import logging

from openbbs_middleware.api import reply_post


class TestReplyPost(unittest.TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_reply_post(self):
        params = {}

        err, results = reply_post.reply_post(params)

        assert err is None
