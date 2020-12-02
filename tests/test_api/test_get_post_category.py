# -*- coding: utf-8 -*-

import unittest
import logging

from openbbs_middleware.api import get_post_category


class TestGetPostCategory(unittest.TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_get_post_category(self):

        params = {}

        err, results = get_post_category.get_post_category(params)

        assert err is None
