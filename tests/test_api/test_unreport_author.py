# -*- coding: utf-8 -*-

import unittest
import logging

from openbbs_middleware.api import unreport_author


class TestUnreportAuthor(unittest.TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_unreport_author(self):
        params = {}
        err, results = unreport_author.unreport_author(params)

        assert err is None
