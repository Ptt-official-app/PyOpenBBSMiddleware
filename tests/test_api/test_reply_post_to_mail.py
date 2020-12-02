# -*- coding: utf-8 -*-

import unittest
import logging

from openbbs_middleware.api import reply_post_to_mail


class TestReplyPostToMail(unittest.TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_reply_post_to_mail(self):
        params = {}

        err, results = reply_post_to_mail.reply_post_to_mail(params)

        assert err is None
