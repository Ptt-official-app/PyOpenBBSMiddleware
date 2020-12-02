# -*- coding: utf-8 -*-

import unittest
import logging

from openbbs_middleware.api import forward_post_to_mail


class TestForwardPostToMail(unittest.TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_forward_post_to_mail(self):
        params = {}

        err, results = forward_post_to_mail.forward_post_to_mail(params)

        assert err is None
