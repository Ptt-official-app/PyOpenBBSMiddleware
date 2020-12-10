# -*- coding: utf-8 -*-

import unittest
import logging

from openbbs_middleware import cfg
from openbbs_middleware.api import find_board_by_name

from unittest import mock
from tests.mock import mocked_requests_post
import mongomock
import pyutil_mongo
from openbbs_middleware.http_server import util_flask
from openbbs_middleware.main import _with_app_prefix


@mock.patch('requests.post', side_effect=mocked_requests_post)
class TestFindBoardByName(unittest.TestCase):

    def setUp(self):
        self.app = util_flask.app

        pass

    def tearDown(self):
        pass

    @mongomock.patch(servers=(('localhost', 27017),))
    def test_find_board_by_name(self, the_mock):
        params = {
            'name': ''
        }

        with self.app.test_request_context(_with_app_prefix(find_board_by_name.ROUTE), environ_base={'REMOTE_ADDR': '10.1.2.3'}, headers={'Authorization': 'bearer init_register'}):
            self.app.preprocess_request()

            err, ret = find_board_by_name.find_board_by_name(params)
            cfg.logger.info('after find_board_by_name: e: %s ret: %s', err, ret)

            assert err is None
