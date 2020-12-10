# -*- coding: utf-8 -*-

import unittest
import logging

from openbbs_middleware import cfg
from openbbs_middleware.http_server import util_flask
from openbbs_middleware.api import find_board_by_name
from openbbs_middleware.deserialize import deserialize_board_list
from openbbs_middleware.mock.board_list import backend_board_list, board_list
from openbbs_middleware.main import _with_app_prefix

from unittest import mock
from tests.mock import mocked_requests_post
import mongomock
import pyutil_mongo


@mock.patch('requests.post', side_effect=mocked_requests_post)
class TestDeserializeBoardList(unittest.TestCase):

    def setUp(self):
        self.app = util_flask.app
        pass

    def tearDown(self):
        pass

    @mongomock.patch(servers=(('localhost', 27017),))
    def test_deserialize_board_list(self, the_mock):
        with self.app.test_request_context(_with_app_prefix(find_board_by_name.ROUTE), environ_base={'REMOTE_ADDR': '10.1.2.3'}, headers={'Authorization': 'bearer init_register'}):
            self.app.preprocess_request()

            backend_results = backend_board_list()
            cfg.logger.info('test_deserialize_board_list: backend_result: %s', type(backend_results))

            err, results = deserialize_board_list.deserialize_board_list(backend_results)

            self.assertEqual(err, None)

            expected = board_list()

            self.assertEqual(expected, results)
