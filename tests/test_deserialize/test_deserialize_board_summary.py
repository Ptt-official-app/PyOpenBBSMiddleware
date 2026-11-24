# -*- coding: utf-8 -*-

import unittest
import logging

from openbbs_middleware.deserialize import deserialize_board_summary
from openbbs_middleware.http_server import util_flask
from openbbs_middleware.main import _with_app_prefix
from openbbs_middleware.mock.board_summary import backend_board_summary, board_summary

import mongomock


class TestDeserializeBoardSummary(unittest.TestCase):

    def setUp(self):
        self.app = util_flask.app

    def tearDown(self):
        pass

    @mongomock.patch(servers=(('localhost', 27017),))
    def test_deserialize_board_summary_without_read_map(self):
        with self.app.test_request_context(_with_app_prefix('/Board/summary/testBoard')):
            self.app.preprocess_request()

            err, result = deserialize_board_summary.deserialize_board_summary(backend_board_summary())

            self.assertEqual(err, None)
            self.assertEqual(board_summary(), result)
