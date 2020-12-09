# -*- coding: utf-8 -*-

from openbbs_middleware.backend.routes import LOGIN, REGISTER, LOAD_GENERAL_BOARDS
from openbbs_middleware import cfg

from openbbs_middleware.mock.board_list import backend_board_list

import logging


def mocked_requests_post(*args, **kwargs):
    class MockResponse:
        def __init__(self, json_data, status_code, text):
            self.json_data = json_data
            self.status_code = status_code
            self.text = text

        def json(self):
            return self.json_data

    ptt_server = cfg.config['ptt_server']

    logging.info('mocked_requests_post: args: %s kwargs: %s', args, kwargs)
    if args[0] == ptt_server + REGISTER:
        return MockResponse({"access_token": "init_register"}, 200, '')
    elif args[0] == ptt_server + LOGIN:
        return MockResponse({"access_token": "init_login"}, 200, '')
    elif args[0] == ptt_server + LOAD_GENERAL_BOARDS:
        return MockResponse(backend_board_list(), 200, '')

    return MockResponse(None, 404, '')
