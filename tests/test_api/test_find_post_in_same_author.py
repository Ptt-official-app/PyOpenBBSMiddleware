# -*- coding: utf-8 -*-

import unittest
import logging

from openbbs_middleware.api import find_post_in_same_author


class TestFindPostInSameAuthor(unittest.TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_find_post_in_same_author(self):

        params = {}

        err, results = find_post_in_same_author.find_post_in_same_author(params)

        assert err is None
