# -*- coding: utf-8 -*-

import unittest
import logging
import tempfile

from http.cookies import SimpleCookie

from openbbs_middleware import cfg
from openbbs_middleware.main import _with_app_prefix
from openbbs_middleware.http_server import util_flask

from openbbs_middleware import main
from openbbs_middleware.utils.util_http import parse_cookies

from openbbs_middleware.api import register_client
from openbbs_middleware.api import account_register

from unittest import mock
from tests.mock import mocked_requests_post
import mongomock
import pyutil_mongo


@mock.patch('requests.post', side_effect=mocked_requests_post)
class TestMain(unittest.TestCase):
    def setUp(self):
        self.app = util_flask.app

    def tearDown(self):
        pass

    def test_index(self, the_mock):
        '''
        test_index
        '''
        with self.app.test_client() as c:
            ret = c.get('/')
        self.assertEqual(401, ret.status_code)

    @mongomock.patch(servers=(('localhost', 27017),))
    def test_index2(self, the_mock):
        '''
        test_index
        '''
        with self.app.test_client() as c:

            client_id = 'test_client_id'
            client_secret = 'test_client_secret'
            ret = c.post(_with_app_prefix(register_client.ROUTE), json={'client_id': client_id, 'client_secret': client_secret}, environ_base={'REMOTE_ADDR': '10.1.2.3'})
            self.assertEqual(200, ret.status_code)

            params = {
                'client_id': client_id,
                'client_secret': client_secret,
                'username': 'SYSOP',
                'password': '123123',
                'password_confirm': '123123',
                'over18': True,
            }
            ret = c.post(_with_app_prefix(account_register.ROUTE), json=params, environ_base={'REMOTE_ADDR': '10.1.2.3'})
            self.assertEqual(200, ret.status_code)

            data = ret.json

            access_token = data.get('access_token', '')

            headers = {
                'Authorization': 'bearer %s' % (access_token),
            }

            cfg.logger.info('to get /: data: %s access_token: %s headers: %s', data, access_token, headers)

            ret = c.get('/', environ_base={'REMOTE_ADDR': '10.1.2.3'}, headers=headers)
            self.assertEqual(200, ret.status_code)
