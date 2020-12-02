# -*- coding: utf-8 -*-

import unittest
import logging
import tempfile

from http.cookies import SimpleCookie

from openbbs_middleware import cfg
from openbbs_middleware.http_server import util_flask

from openbbs_middleware import main
from openbbs_middleware.utils.util_http import parse_cookies

import mongomock
import pyutil_mongo
import pyutil_cfg
from unittest import mock
import requests


def mocked_requests_post(*args, **kwargs):
    class MockResponse:
        def __init__(self, json_data, status_code, text):
            self.json_data = json_data
            self.status_code = status_code
            self.text = text

        def json(self):
            return self.json_data

    if args[0] == 'http://localhost:3456/register':
        return MockResponse({"Jwt": "main_register"}, 200, '')
    elif args[0] == 'http://localhost:3456/login':
        return MockResponse({"Jwt": "main_register"}, 200, '')

    return MockResponse(None, 404)


class TestMain(unittest.TestCase):
    def setUp(self):
        self.app = util_flask.app

    def tearDown(self):
        pass

    def test_index(self):
        '''
        test_index
        '''
        ret = self.app.get('/Account/logout')
        self.assertEqual(302, ret.status_code)

        ret = self.app.get('/')
        self.assertEqual(401, ret.status_code)

    @mock.patch('requests.post', side_effect=mocked_requests_post)
    def test_index2(self, mock_post):
        '''
        test_index after login
        '''
        logging.info('cfg.config: %s', cfg.config)

        ret = self.app.get('/Account/logout')
        self.assertEqual(302, ret.status_code)

        ret = self.app.get('/Account/register')
        self.assertEqual(200, ret.status_code)
        the_headers = ret.headers

        headers = {
        }

        data = {
            'user_id': 'test_user_id',
            'password': '123123',
            'password_confirm': '123123',
            'over18': True,
        }

        ret = self.app.post('/Account/register', data=data, headers=headers)
        self.assertEqual(302, ret.status_code)

        cfg.logger.info('after register: headers: %s content :%s', ret.headers, ret.data.decode('utf-8'))

        ret = self.app.post('/Account/login')
        self.assertEqual(302, ret.status_code)

        ret = self.app.get('/')
        self.assertEqual(200, ret.status_code)

    def test_index3(self):
        cfg.logger.debug('headers: %s', cfg.config['test_headers'])
        ret = self.app.get('/', headers=cfg.config['test_headers'])
        self.assertEqual(200, ret.status_code)
