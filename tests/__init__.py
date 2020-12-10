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
import pyutil_mongo

import mongomock

from unittest import mock
import requests


@mongomock.patch(servers=(('localhost', 27017),))
def setup():
    cfg.init('tests/test.ini')

    util_flask.init_flask()

    util_flask.app.testing = True

    pyutil_mongo.db_update('client', {'client_id': 'test_client_id'}, {'client_secret': 'test_client_secret'})


def teardown():
    pass
