# -*- coding: utf-8 -*-

import flask
import pyutil_mongo

from openbbs_middleware import cfg
from openbbs_middleware.schema.user_read_board import serialize_user_read_board_idx

from openbbs_middleware.utils.util_time import ts_to_milli_ts


def deserialize_board_summary(serialized, read_map=None):
    board_id = serialized['brdname']
    result = {
        'boardID': board_id,
        'title': serialized['title'],
        'flag': serialized['brdAttr'],
        "boardType": serialized['boardType'],
        "cat": serialized['class'],
        "onlineCount": serialized['nUser'],
        "moderators": serialized['moderators'],
        "reason": serialized['reason'],
        'total': serialized['total'],
    }

    # read
    user_id = flask.g.user
    idx = serialize_user_read_board_idx(user_id, board_id)

    read_milli_ts = 0
    if read_map is not None:
        read_milli_ts = read_map.get(idx, 0)
    else:
        err, db_result = pyutil_mongo.find_one('user_read_board', {'idx': idx})
        if err:
            return err, {}
        read_milli_ts = db_result.get('update_milli_ts', 0)

    result['read'] = read_milli_ts > ts_to_milli_ts(serialized['lastPostTime'])

    return None, result
