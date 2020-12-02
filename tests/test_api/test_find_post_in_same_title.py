# -*- coding: utf-8 -*-

import unittest
import logging

from openbbs_middleware.api import find_post_in_same_title


class TestFindPostInSameTitle(unittest.TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_find_post_in_same_title(self):
        params = {}

        err, results = find_post_in_same_title.find_post_in_same_title(params)

        assert err is None
