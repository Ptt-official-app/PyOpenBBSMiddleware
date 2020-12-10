# -*- coding: utf-8 -*-
"""Summary
"""

from openbbs_middleware import cfg
from openbbs_middleware.constants import MAX_LIST
from openbbs_middleware.backend.routes import LOAD_GENERAL_BOARDS
from openbbs_middleware.utils.util_http import http_post
from openbbs_middleware.deserialize.deserialize_board_list import deserialize_board_list
from openbbs_middleware.utils.util_type import _int

ROUTE = '/board/search'


def find_board_by_name(params):
    '''

    Args:
        params (TYPE): Description

    Returns:
        TYPE: Description
    '''
    keyword = params.get('name', '')
    start_idx = params.get('startIdx', '')
    err, the_max = _int(params.get('max', MAX_LIST))
    if err:
        return err, {}

    if the_max >= MAX_LIST:
        the_max = MAX_LIST

    url = cfg.config.get('ptt_server', '') + LOAD_GENERAL_BOARDS

    # serialize params
    data = {
        'start_idx': start_idx,
        'max': the_max,
        'keyword': keyword,
    }
    err, http_results = http_post(url, data)
    if err:
        return err, {}

    err, results = deserialize_board_list(http_results)
    if err:
        return err, {}

    return None, results
