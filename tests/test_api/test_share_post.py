# -*- coding: utf-8 -*-

import unittest
import logging

from openbbs_middleware.api import share_post


class TestSharePost(unittest.TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_share_post(self):

        params = {}

        err, results = share_post.share_post(params)

        assert err is None
