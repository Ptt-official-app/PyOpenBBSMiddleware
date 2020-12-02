# -*- coding: utf-8 -*-

import unittest
import logging

from openbbs_middleware.api import get_popular_post


class TestGetPopularPost(unittest.TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_get_popular_post(self):

        params = {}

        err, results = get_popular_post.get_popular_post(params)

        assert err is None
