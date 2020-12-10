# -*- coding: utf-8 -*-

from openbbs_middleware import cfg
from openbbs_middleware.utils.util_http import http_post
from openbbs_middleware.backend.routes import LOGIN


def validate_user(user_id, password):
    """validate user

    Args:
        user_id (TYPE): Description
        password (TYPE): Description

    Returns:
        TYPE: Description
    """
    url = cfg.config.get('ptt_server', '') + LOGIN

    err, result = http_post(url, {'username': user_id, 'password': password})

    if err:
        return err, ''

    jwt = result.get('access_token', '')

    return None, jwt
