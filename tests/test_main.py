# -*- coding: utf-8 -*-

import unittest
import logging
import tempfile

from openbbs_middleware import cfg
from openbbs_middleware.http_server import util_flask
from openbbs_middleware.http_server.util_flask import app

from openbbs_middleware import main


class TestMain(unittest.TestCase):
    def setUp(self):
        util_flask.init_flask()

        self.app = app.test_client()
        self.app.testing = True

    def tearDown(self):
        pass

    def test_index(self):
        '''
        test_index
        '''
        '''
        logging.warning('cfg.config: %s', cfg.config)
        ret = self.app.get('/')
        self.assertEqual(200, ret.status_code)
        the_json = ret.get_json()
        data = the_json.get('data', {})
        logging.info('ret: %s the_json: %s', ret, the_json)
        self.assertTrue(the_json.get('success'))
        self.assertTrue('index' in data)
        '''
