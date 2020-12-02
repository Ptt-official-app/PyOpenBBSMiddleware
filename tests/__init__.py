# -*- coding: utf-8 -*-

import gevent.monkey
gevent.monkey.patch_all()

import logging

import pyutil_cfg

from openbbs_middleware import cfg
from openbbs_middleware.http_server import util_flask
from openbbs_middleware.utils.util_http import parse_csrftoken, parse_cookies

import flask

import mongomock

@mongomock.patch(servers=(('localhost', 27017),))
def setup():
    pyutil_cfg.init = _mock_cfg_init

    cfg.init('')
    cfg.logger = logging

    util_flask.init_flask()

    util_flask.app = util_flask.app.test_client()
    util_flask.app.testing = True

    ret = util_flask.app.post('/Account/register', data={'email': 'temp2@temp.com', 'password': '12345678', 'password_confirm': '12345678'})

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
    }

    return logging, config


def teardown():
    pass
