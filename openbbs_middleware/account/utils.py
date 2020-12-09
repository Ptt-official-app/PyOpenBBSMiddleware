# -*- coding: utf-8 -*-

import re

import pyutil_mongo

from openbbs_middleware import cfg
from openbbs_middleware.utils.util_time import get_current_milli_ts


def is_valid_user_id(user_id):
    match = re.search(r'[^0-9A-Za-z]', user_id)
    return match is None


def is_valid_client(client_id, client_secret):
    err, db_results = pyutil_mongo.db_find('client', {'client_id': client_id, 'client_secret': client_secret})
    if err is not None:
        return False

    if not db_results:
        return False

    return True


def post_login(user_id, jwt, is_register=False):
    current_milli_ts = get_current_milli_ts()

    update_data = {
        'login_milli_ts': current_milli_ts,
        'update_milli_ts': current_milli_ts,
    }
    if is_register:
        update_data['register_milli_ts'] = current_milli_ts

    err, results = pyutil_mongo.db_update('user', {'user_id': user_id}, update_data)
    if err:
        return err

    err, results = pyutil_mongo.db_update('access_token', {'access_token': jwt}, {'user_id': user_id, 'update_milli_ts': current_milli_ts})
    if err:
        return err

    return None
