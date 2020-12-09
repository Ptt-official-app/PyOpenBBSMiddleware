# -*- coding: utf-8 -*-
"""Summary
"""

from flask import request

import pyutil_mongo

from openbbs_middleware import cfg
from openbbs_middleware.utils.util_http import http_post
from openbbs_middleware.utils.util_time import get_current_milli_ts


def register_user(user_id, password, email, nickname, realname, career, address, over18):
    """register user

    Args:
        user_id (TYPE): Description
        password (TYPE): Description
        nickname (TYPE): Description
        realname (TYPE): Description
        career (TYPE): Description
        address (TYPE): Description
        over18 (TYPE): Description

    Returns:
        TYPE: Description
    """
