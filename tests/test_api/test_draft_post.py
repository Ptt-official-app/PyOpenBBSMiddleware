# -*- coding: utf-8 -*-

import unittest
import logging

from openbbs_middleware.api import draft_post


class TestDraftPost(unittest.TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_draft_post(self):
        params = {
        }

        err, result = draft_post.draft_post(params)

        assert err is None