# -*- coding: utf-8 -*-

import pyutil_mongo

from openbbs_middleware import cfg
from openbbs_middleware.utils.util_time import get_current_milli_ts

ROUTE = '/register/client'


def register_client(params):
    client_id = params.get('client_id', '')
    client_secret = params.get('client_secret', '')

    if not client_id:
        return Exception('invalid client'), {}

    update_milli_ts = get_current_milli_ts()

    err, result = pyutil_mongo.db_update('client', {'client_id': client_id}, {'client_secret': client_secret, 'update_milli_ts': update_milli_ts})

    return err, {'success': True}
