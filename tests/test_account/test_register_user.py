# -*- coding: utf-8 -*-

import unittest
from unittest import mock

import logging

from openbbs_middleware.account import register_user
from openbbs_middleware.backend.routes import REGISTER
from openbbs_middleware.http_server import util_flask
from openbbs_middleware import cfg

from tests.mock import mocked_requests_post


@mock.patch('requests.post', side_effect=mocked_requests_post)
class TestRegisterUser(unittest.TestCase):

    def setUp(self):
        self.app = util_flask.app

    def tearDown(self):
        pass

    def test_register_user(self, the_mock):
        with self.app.test_request_context('?limit=1&offset=2'):
            err, jwt = register_user.register_user(
                'test_user100',
                'test_passwd',
                'test_email',
                'test_nickname',
                'test_realname',
                'test_career',
                'test_address',
                True,
            )

        cfg.logger.info('after register_user: e: %s jwt: %s', err, jwt)
        assert err is None
        assert jwt == 'init_register'

