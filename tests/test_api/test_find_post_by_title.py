# -*- coding: utf-8 -*-

import unittest
import logging

from openbbs_middleware.api import find_post_by_title


class TestFindPostByTitle(unittest.TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_find_post_by_title(self):
        params = {}

        err, result = find_post_by_title.find_post_by_title(params)

        assert err is None
