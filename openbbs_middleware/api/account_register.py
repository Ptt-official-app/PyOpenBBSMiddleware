# -*- coding: utf-8 -*-

from openbbs_middleware import cfg
from openbbs_middleware.account.utils import is_valid_client, is_valid_user_id, post_login
from openbbs_middleware.account.register_user import register_user

ROUTE = '/Account/register'


def account_register(params):
    client_id = params.get('client_id', '')
    client_secret = params.get('client_secret', '')
    if not is_valid_client(client_id, client_secret):
        return Exception('invalid client'), {}

    user_id = params.get('username', '')
    if not is_valid_user_id(user_id):
        return Exception('invalid user'), {}

    password = params.get('password', '')
    password_confirm = params.get('password_confirm', '')
    if password != password_confirm:
        return Exception('invalid params'), {}

    over18 = params.get('over18', False)
    email = params.get('email', '')
    nickname = params.get('nickname', '')
    realname = params.get('realname', '')
    career = params.get('career', '')
    address = params.get('address', '')

    err, jwt = register_user(user_id, password, email, nickname, realname, career, address, over18)
    if err:
        return err, {}

    err = post_login(user_id, jwt)
    if err:
        return err, {}

    return None, {'access_token': jwt, 'token_type': 'bearer'}
