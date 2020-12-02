# -*- coding: utf-8 -*-
#
# From flask_security.registerable
#
# This is to skip the requirement of password settings.
#
# XXX
# We don't record email address for now.
# Need some method to be able to send confirmation letter.

import pyutil_mongo

from flask_security.registerable import _datastore

from openbbs_middleware import cfg
from openbbs_middleware.utils.util_time import get_current_milli_ts

_VALID_USER_MODEL_KEY_SET = set([
    'user_id',
    'jwt',
    'uid',
])


def register_user(registration_form):
    """
    Calls datastore to create user, triggers post-registration logic
    (e.g. sending confirmation link, sending registration mail)
    :param registration_form: form with user registration data
    :return: user instance
    """

    user_model_kwargs = registration_form.to_dict(only_user=True)

    user_model_kwargs = {k: v for k, v in user_model_kwargs.items() if k in _VALID_USER_MODEL_KEY_SET}

    user = _datastore.create_user(**user_model_kwargs)

    err, db_results = pyutil_mongo.db_find('user', {})

    '''
    confirmation_link, token = None, None
    if _security.confirmable:
        confirmation_link, token = generate_confirmation_link(user)
        do_flash(*get_message("CONFIRM_REGISTRATION", email=user.email))

    user_registered.send(
        app._get_current_object(),
        user=user,
        confirm_token=token,
        form_data=registration_form.to_dict(only_user=False),
    )

    if config_value("SEND_REGISTER_EMAIL"):
        _security._send_mail(
            config_value("EMAIL_SUBJECT_REGISTER"),
            user.email,
            "welcome",
            user=user,
            confirmation_link=confirmation_link,
        )
    '''

    return user
