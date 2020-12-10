# -*- coding: utf-8 -*-

user_read_board = {
    'idx': str,
    'update_milli_ts': int,
}


def serialize_user_read_board_idx(user_id, board_id):
    return '%s:%s' % (user_id, board_id)
