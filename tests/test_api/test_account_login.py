# -*- coding: utf-8 -*-

import unittest
import logging

from openbbs_middleware.api import account_login
from openbbs_middleware.api import account_register
from openbbs_middleware import cfg
from openbbs_middleware.main import _with_app_prefix
from openbbs_middleware.http_server import util_flask

from unittest import mock
from tests.mock import mocked_requests_post
import mongomock
import pyutil_mongo


@mock.patch('requests.post', side_effect=mocked_requests_post)
class TestAccountLogin(unittest.TestCase):

    def setUp(self):
        self.app = util_flask.app

    def tearDown(self):
        pass

    @mongomock.patch(servers=(('localhost', 27017),))
    def test_login(self, the_mock):
        with self.app.test_request_context(_with_app_prefix(account_login.ROUTE), environ_base={'REMOTE_ADDR': '10.1.2.3'}):
            err, ret = account_login.account_login({'client_id': 'test_client_id', 'client_secret': 'test_client_secret'})

        assert err is not None

        params = {
            'client_id': 'test_client_id',
            'client_secret': 'test_client_secret',

            'username': 'testuser3',
            'password': 'test_password',
            'password_confirm': 'test_password',
            'over18': True,
        }

        pyutil_mongo.db_update('client', {'client_id': 'test_client_id'}, {'client_secret': 'test_client_secret'})

        with self.app.test_request_context(_with_app_prefix(account_login.ROUTE), environ_base={'REMOTE_ADDR': '10.1.2.3'}):
            err, ret = account_register.account_register(params)
            assert err is None

            err, ret = account_login.account_login({'client_id': 'test_client_id', 'client_secret': 'test_client_secret', 'username': 'testuser3', 'password': 'test_password'})

        assert err is None
        assert 'access_token' in ret
