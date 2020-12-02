# -*- coding: utf-8 -*-

import unittest
import logging

from openbbs_middleware.api import publish_post


class TestPublishPost(unittest.TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_publish_post(self):
        params = {}

        err, results = publish_post.publish_post(params)

        assert err is None
