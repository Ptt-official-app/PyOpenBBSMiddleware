# -*- coding: utf-8 -*-

import unittest
import logging

from openbbs_middleware.api import find_post_by_author


class TestFindPostByAuthor(unittest.TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_find_post_by_author(self):

        params = {
        }

        err, result = find_post_by_author.find_post_by_author(params)

        assert err is None
