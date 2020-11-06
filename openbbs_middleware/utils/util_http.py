# -*- coding: utf-8 -*-

import rapidjson as json
import requests


def http_post(url, data=None, is_json=True):

    if is_json and type(data) == dict:
        data = json.dumps(data)

    r = requests.post(url, data=data)

    if r.status_code != 200:
        return Exception('status_code: %s' % (r.status_code)), {'err': r.text}

    try:
        the_struct = r.json()
    except Exception as e:
        return e, {}

    return None, the_struct
