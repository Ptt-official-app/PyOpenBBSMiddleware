# -*- coding: utf-8 -*-

from openbbs_middleware import cfg
from openbbs_middleware.account.validate_user import validate_user
from openbbs_middleware.account.utils import is_valid_client, post_login

ROUTE = '/Account/login'


def account_login(params):
    client_id = params.get('client_id', '')
    client_secret = params.get('client_secret', '')
    if not is_valid_client(client_id, client_secret):
        return Exception('invalid client'), {}

    user_id = params.get('username', '')
    password = params.get('password', '')

    err, jwt = validate_user(user_id, password)
    if err:
        return err, {}

    err = post_login(user_id, jwt)
    if err:
        return err, {}

    return None, {'access_token': jwt}
