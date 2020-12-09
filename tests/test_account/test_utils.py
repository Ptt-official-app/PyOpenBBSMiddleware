# -*- coding: utf-8 -*-

import unittest
import logging
import mongomock
import pyutil_mongo

from openbbs_middleware.account import utils
from openbbs_middleware import cfg


class TestUtils(unittest.TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_is_valid_user_id(self):
        assert utils.is_valid_user_id('abcdef')
        assert utils.is_valid_user_id('012345678901')
        assert not utils.is_valid_user_id('asdf!@#$')
        assert not utils.is_valid_user_id(':".asdfsadf')

    @mongomock.patch(servers=(('localhost', 27017),))
    def test_is_valid_client(self):
        pyutil_mongo.db_update('client', {'client_id': 'test_client_id'}, {'client_secret': 'test_client_secret'})

        assert utils.is_valid_client('test_client_id', 'test_client_secret')
        assert not utils.is_valid_client('test_client_id', 'test_not-exists')
        assert not utils.is_valid_client('test_not-exists', 'test_client_secret')
        assert not utils.is_valid_client('test_not-exists', 'test_not-exists')

        pyutil_mongo.db_force_remove('client', {})
