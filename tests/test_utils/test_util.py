# -*- coding: utf-8 -*-

import unittest
import logging

from openbbs_middleware.utils import util


class TestUtil(unittest.TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_flatten_errors_no_error(self):
        err, the_list = util.flatten_errors([(None, 'a'), (None, 'b')])

        self.assertIsNone(err)
        self.assertEqual(['a', 'b'], the_list)

    def test_flatten_errors_with_error(self):
        err, the_list = util.flatten_errors([(None, 'a'), (Exception('e1'), 'b')])

        self.assertEqual('1:e1', err)
        self.assertEqual(['a', 'b'], the_list)
