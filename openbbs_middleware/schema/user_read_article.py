# -*- coding: utf-8 -*-


user_read_article = {
    'idx': str,
    'update_milli_ts': int,
}


def serialize_user_read_article_idx(user_id, article_id):
    return '%s:%s' % (user_id, article_id)
