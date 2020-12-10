# -*- coding: utf-8 -*-

from openbbs_middleware import cfg
from openbbs_middleware.utils.util_http import http_post
from openbbs_middleware.backend.routes import REGISTER


def register_user(user_id, password, email, nickname, realname, career, address, over18):
    url = cfg.config.get('ptt_server', '') + REGISTER

    params = {
        'username': user_id,
        'password': password,

        'email': email,
        'nickname': nickname,
        'realname': realname,
        'career': career,
        'address': address,
        'over18': over18,
    }
    err, result = http_post(url, params)
    if err:
        return err, result.get('err', '')

    jwt = result.get('access_token', '')

    return None, jwt
