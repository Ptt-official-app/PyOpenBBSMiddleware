# -*- coding: utf-8 -*-

import gevent.monkey
gevent.monkey.patch_all()

import logging

import pyutil_cfg

from openbbs_middleware import cfg


def setup():
    pyutil_cfg.init = _mock_cfg_init

    cfg.init('')


def _mock_cfg_init(ini_filename, log_ini_filename='', params=None):
    config = {
        'mongo_protocol': 'mongomock',
    }

    return logging, config


def teardown():
    pass
