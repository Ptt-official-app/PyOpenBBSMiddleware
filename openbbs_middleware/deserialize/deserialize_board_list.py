# -*- coding: utf-8 -*-

from openbbs_middleware import cfg
from openbbs_middleware.utils.util import flatten_errors
from openbbs_middleware.deserialize.deserialize_board_summary import deserialize_board_summary

from openbbs_middleware.schema.user_read_board import serialize_user_read_board_idx

import flask
import pyutil_mongo

import traceback


def deserialize_board_list(serialized):
    the_list = serialized.get('boards', [])

    # get user_read_board
    user_id = flask.g.user
    idxes = [serialize_user_read_board_idx(user_id, each['brdname']) for each in the_list]
    err, db_results = pyutil_mongo.db_find('user_read_board', {'idx': {'$in': idxes}})
    if err:
        return err, {}

    read_map = {each['idx']: each['update_milli_ts'] for each in db_results}

    the_list_with_errs = [deserialize_board_summary(each, read_map) for each in the_list]
    err, the_list = flatten_errors(the_list_with_errs)
    if err:
        return err, {}

    next_idx = serialized.get('next_bid')
    if next_idx is None:
        return Exception('invalid serialized'), {}

    return None, {'list': the_list, 'nextIdx': next_idx}
