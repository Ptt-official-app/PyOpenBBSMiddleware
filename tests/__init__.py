# -*- coding: utf-8 -*-

import gevent.monkey
gevent.monkey.patch_all()

import logging

import pyutil_cfg

from openbbs_middleware import cfg
from openbbs_middleware.http_server import util_flask
from openbbs_middleware.utils.util_http import parse_csrftoken, parse_cookies

import flask
import requests

import mongomock

from unittest import mock
import requests


# https://stackoverflow.com/questions/15753390/how-can-i-mock-requests-and-the-response
def mocked_requests_post(*args, **kwargs):
    class MockResponse:
        def __init__(self, json_data, status_code, text):
            self.json_data = json_data
            self.status_code = status_code
            self.text = text

        def json(self):
            return self.json_data

    if args[0] == 'http://localhost:3456/register':
        return MockResponse({"Jwt": "init_register"}, 200, '')
    elif args[0] == 'http://localhost:3456/login':
        return MockResponse({"Jwt": "init_login"}, 200, '')

    return MockResponse(None, 404)


@mock.patch('requests.post', side_effect=mocked_requests_post)
@mongomock.patch(servers=(('localhost', 27017),))
def setup(mock_post):
    pyutil_cfg.init = _mock_cfg_init

    cfg.init('')
    cfg.logger = logging

    util_flask.init_flask()

    util_flask.app = util_flask.app.test_client()
    util_flask.app.testing = True

    data = {
        'user_id': 'test_user_id',
        'password': '123123',
        'password_confirm': '123123',
        'over18': True,
    }

    ret = util_flask.app.post('/Account/register', data=data)

    cfg.logger.info('test/__init__: after register: ret: (%s/%s/%s)', ret.status_code, ret.headers, ret.data.decode('utf-8'))

    the_headers = ret.headers
    cookies = parse_cookies(the_headers.get_all('Set-Cookie'))
    session = cookies.get('session', '')

    headers = {
        'Cookie': 'session=%s;' % (session)
    }

    ret = util_flask.app.post('/Account/login', data={'email': 'temp@temp.com', 'password': '12345678'})

    the_json = ret.get_json()
    the_headers = ret.headers
    cookies = parse_cookies(the_headers.get_all('Set-Cookie'))
    cfg.logger.info('after parse cookies: cookies: %s', cookies)

    login_session = cookies.get('session', '')
    if login_session != '':
        session = login_session

    cfg.config['test_session'] = session
    cfg.config['test_headers'] = {
        'Cookie': 'session=%s' % (session),
    }


def _mock_cfg_init(ini_filename, log_ini_filename='', params=None):
    config = {
        'mongo_protocol': 'mongomock',
        'flask_static_folder': './static',
        'ptt_server': 'http://localhost:3456',
    }

    return logging, config


def teardown():
    pass
