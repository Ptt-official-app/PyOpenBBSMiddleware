# -*- coding: utf-8 -*-
"""Summary
"""

import requests
from flask_security.forms import LoginForm as SecurityLoginForm, StringField, get_form_field_label
from flask_security import UserMixin

from openbbs_middleware.http_server.utils import get_ip
from openbbs_middleware.http_server.utils import validate_user

import pyutil_mongo


class User(UserMixin):
    """User for flask-security.

    Attributes:
        id (str): Description
        is_active (bool): Description
    """

    is_active = True
    id = ''


class LoginForm(SecurityLoginForm):
    """customized login form. validating with backend.

    Attributes:
        jwt (TYPE): Description
        user (TYPE): Description
        username (TYPE): Description
    """

    username = StringField(
        get_form_field_label("username"), validators=[],
    )

    jwt = StringField(
        get_form_field_label("jwt"), validators=[],
    )

    def validate(self):
        """validate user.

        Returns:
            TYPE: Description
        """
        username = self.data.get('username', '')
        password = self.data.get('password', '')
        ip = get_ip()

        err, jwt = validate_user(username, password, ip)
        if err:
            return False

        err, result = pyutil_mongo.db_find_one('user', {'user_id': username}, ["_id"])
        if err:
            return False

        the_id = str(result.get("_id", ''))

        self.user = User()
        self.user.id = the_id
        self.user.is_active = True
        self.user.jwt = jwt

        return True
