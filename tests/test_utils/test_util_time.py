# -*- coding: utf-8 -*-

import unittest
import logging

from openbbs_middleware.utils import util_time

import time


class TestUtilTime(unittest.TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_get_current_milli_ts(self):
        current_ts = time.time()
        current_milli_ts = util_time.get_current_milli_ts()

        current_ts2 = time.time()

        assert current_milli_ts >= int(current_ts * 1000)
        assert current_ts2 * 1000 >= current_milli_ts
