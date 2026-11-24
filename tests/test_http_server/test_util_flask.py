# -*- coding: utf-8 -*-

import unittest
import logging

from openbbs_middleware.http_server import util_flask


class TestUtilFlask(unittest.TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_default_secrets_are_not_well_known(self):
        self.assertNotEqual('default_flask_secret_key', util_flask.app.config['SECRET_KEY'])
        self.assertNotEqual('default_flask_secret_salt', util_flask.app.config['SECURITY_PASSWORD_SALT'])
        self.assertGreaterEqual(len(util_flask.app.config['SECRET_KEY']), 32)
        self.assertGreaterEqual(len(util_flask.app.config['SECURITY_PASSWORD_SALT']), 32)
