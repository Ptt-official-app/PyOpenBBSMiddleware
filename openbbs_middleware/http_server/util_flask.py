# -*- coding: utf-8 -*-
"""flask

Attributes:
    app (App): Flask app
    csrf (CSRF): csrf protection
    login_manager (LoginManager): Flask-Login manager
"""

##########
# XXX
# patch register_user
##########
from functools import wraps
from flask_security import registerable
from flask_security import views
from openbbs_middleware.http_server.register_user import register_user
registerable.register_user = register_user
views.register_user = register_user

from functools import update_wrapper
from bson.objectid import ObjectId
import rapidjson as json

import flask
from flask import Flask, request, make_response, current_app

import flask_login
from flask.json import jsonify

from flask_mongoengine import MongoEngine
from flask_security import Security, MongoEngineUserDatastore, UserMixin, RoleMixin
from flask_mail import Mail

from flask_wtf.csrf import CSRFProtect
import flask_security

from mongoengine import StringField, ListField, BooleanField, DateTimeField, EmbeddedDocumentField, EmbeddedDocument


import pyutil_mongo
import traceback
from datetime import timedelta

from werkzeug.middleware.proxy_fix import ProxyFix
from openbbs_middleware import cfg

from openbbs_middleware.http_server.login_form import LoginForm
from openbbs_middleware.http_server.confirm_register_form import ConfirmRegisterForm
from openbbs_middleware.http_server.register_form import RegisterForm

###
# customized register_user (no need to store password.)
###

app = Flask(__name__.split('.')[0])
app.wsgi_app = ProxyFix(app.wsgi_app, x_proto=1, x_host=1, x_port=1)
csrf = CSRFProtect()
csrf.init_app(app)

login_manager = flask_login.LoginManager()
login_manager.init_app(app)


def process_json():
    return request.get_json(force=True)


def process_params():
    """Summary

    Returns:
        TYPE: Description
    """
    qs_dict = request.values
    form_dict = request.form

    result = {}
    for key, val in qs_dict.items():
        result_val = val if not isinstance(val, list) else val[-1]
        result[key] = result_val

    for key, val in form_dict.items():
        result_val = val if not isinstance(val, list) else val[-1]
        result[key] = result_val

    return result


def process_result(err, the_dict, status_code=200, mime='application/json', headers=None):
    """process result

    Args:
        err (Exception): err
        the_dict (dict): result
        status_code (int, optional): status code
        mime (str, optional): mime
        headers (dict, optional): headers

    Returns:
        TYPE: Description
    """
    if headers is None:
        headers = {}

    user = flask.g.user

    username = getattr(user, 'username', None)

    headers['Content-Type'] = mime
    if username is not None:
        headers['X-WEBAUTH-USER'] = username

    if err:
        http_result = {'err': str(err)}
    else:
        http_result = the_dict

    return json.dumps(http_result), status_code, headers


def init_flask():
    """init flask
    """
    _init_config()

    _init_db()


def _init_config():
    """Summary
    """
    flask_secret_key = 'default_flask_secret_key'
    secret_file = cfg.config.get('flask_secret_file', '')
    if secret_file:
        with open(secret_file, 'r') as f:
            flask_secret_key = f.read()

    flask_security_salt = 'default_flask_secret_salt'
    salt_file = cfg.config.get('flask_security_salt_file', '')
    if salt_file:
        with open(salt_file, 'r') as f:
            flask_security_salt = f.read()

    mongo_protocol = cfg.config.get('mongo_protocol', 'mongodb')
    mongo_host = cfg.config.get('mongo_host', 'localhost')
    mongo_port = cfg.config.get('mongo_port', 27017)
    mongo_dbname = cfg.config.get('mongo_dbname', '')
    host = '%s://%s:%s/%s' % (mongo_protocol, mongo_host, mongo_port, mongo_dbname)

    mongo_settings = {
        'db': mongo_dbname,
        'host': host,
        'ssl': cfg.config.get('mongo_ssl', False),
    }
    if mongo_settings['ssl']:
        mongo_settings.update({
            'authSource': '$external',
            'authMechanism': 'MONGODB-X509',
            'ssl_certfile': cfg.config.get('mongo_sslpemkeyfile', None),
            'ssl_ca_certs': cfg.config.get('mongo_sslca', None),
        })

    cfg.logger.info('util_flask._init_config: mongo_settings: %s', mongo_settings)

    app.config.update({
        'SECRET_KEY': flask_secret_key,
        'EXPLAIN_TEMPLATE_LOADING': False,
        'MONGODB_SETTINGS': mongo_settings,
        'SESSION_PROTECTION': 'strong',
        'SECURITY_PASSWORD_HASH': 'sha512_crypt',
        'SECURITY_PASSWORD_SALT': flask_security_salt,
        'SECURITY_RECOVERABLE': False,
        'SECURITY_SEND_REGISTER_EMAIL': False,

        'SECURITY_LOGIN_USER_TEMPLATE': 'login.html',
        'SECURITY_REGISTER_USER_TEMPLATE': 'register_user.html',

        'SECURITY_REGISTERABLE': cfg.config.get('flask_security_registerable', True),
        'SECURITY_CONFIRMABLE': cfg.config.get('flask_security_confirmable', False),
        'SECURITY_LOGIN_URL': '/login',
        'SECURITY_REGISTER_URL': '/register',
        'SECURITY_LOGOUT_URL': '/logout',
        'SECURITY_POST_LOGOUT_VIEW': '/login',
        'SECURITY_EMAIL_SENDER': cfg.config.get('mail_sender', 'noreply@localhost'),
        'MAIL_DEBUG': True,
        'MAIL_SERVER': cfg.config.get('mail_server', 'localhost'),
        'MAIL_DEFAULT_SENDER': cfg.config.get('mail_sender', 'noreply@localhost'),
        'MAIL_PORT': cfg.config.get('mail_port', 25),
        'MAIL_USE_TLS': cfg.config.get('mail_use_tls', False),
        'MAIL_USE_SSL': cfg.config.get('mail_use_ssl', False),
        'MAIL_USER_NAME': cfg.config.get('mail_username', None),
        'MAIL_PASSWORD': cfg.config.get('mail_password', None),
        'WTF_CSRF_ENABLED': False,
    })

    app.static_folder = cfg.config.get('flask_static_folder', None)
    app.template_folder = cfg.config.get('flask_static_folder', None)


def _init_db():
    """init flask-db
    """
    db = MongoEngine(app)

    class Role(db.Document, RoleMixin):
        """Role in flask-security

        Attributes:
            description (TYPE): Description
            name (TYPE): Description
        """

        name = StringField(max_length=80, unique=True)
        description = StringField(max_length=255)

    class EmbeddedRole(EmbeddedDocument, RoleMixin):
        """Embedded-Role in flask-security

        Attributes:
            description (TYPE): Description
            name (TYPE): Description
            permissions (TYPE): Description
        """

        name = StringField(max_length=80)
        description = StringField(max_length=255)
        permissions = StringField()

    class User(db.Document, UserMixin):
        """User in flask-security

        Attributes:
            active (bool): is-active
            jwt (str): jwt
            roles (list): roles
            uid (str): (to be the guid for the user.)
            user_id (str): username.
        """

        user_id = StringField(max_length=1000)
        jwt = StringField(max_length=10000)
        uid = StringField(max_length=1000)
        active = BooleanField(default=True)
        roles = ListField(EmbeddedDocumentField(EmbeddedRole), default=[])

    user_datastore = MongoEngineUserDatastore(db, User, Role)

    Security(app=app, datastore=user_datastore, login_form=LoginForm, confirm_register_form=ConfirmRegisterForm, register_form=RegisterForm)
    Mail(app)

    @app.login_manager.unauthorized_handler
    def unauth_handler():
        """unauth-handler for login-manager

        Returns:
            TYPE: Description
        """
        return jsonify(success=False,
                       data={'login_required': True},
                       message='Authorize please to access this page'), 401

    @app.login_manager.user_loader
    def load_user(the_id):
        """load-user

        Args:
            the_id (str): the-id corresponding to _id in mongodb.

        Returns:
            User: user
        """

        fields = ['user_id', 'jwt']
        the_id = ObjectId(the_id)
        try:
            error, db_result = pyutil_mongo.db_find_one('user', {'_id': the_id}, fields)

            if error:
                cfg.logger.error('unable to find user: e: %s', error)
                return
            if not db_result:
                cfg.logger.error('user not exist')
                return

            user_id = db_result.get('user_id', '')
            jwt = db_result.get('jwt', '')

            return User(user_id=user_id, jwt=jwt)

        except (TypeError, ValueError) as e:
            cfg.logger.error('unable to get user_id: user_id: %s e: %s', user_id, e)
            traceback.print_stack(e)


def crossdomain(origin=None, methods=None, headers=None,
                max_age=None, attach_to_all=True,
                automatic_options=True):
    """crossdomain

        Web-browsers requires matching origin for post-data.
        In the attach-to-all mode (attach-to-all is set to true),
        We set the Allow-Origin as the request-origin if we think
        that the request-origin is ok to access our service.

    Args:
        origin (None, optional): Description
        methods (None, optional): Description
        headers (None, optional): Description
        max_age (None, optional): Description
        attach_to_all (bool, optional): Description
        automatic_options (bool, optional): Description

    Returns:
        TYPE: Description
    """
    if methods is not None:
        methods = ', '.join(sorted(x.upper() for x in methods))
    if headers is not None and not isinstance(headers, str):
        headers = ', '.join(x.upper() for x in headers)
    if origin is not None and not isinstance(origin, str):
        pass
        # origin = str(origin)
    if isinstance(max_age, timedelta):
        max_age = max_age.total_seconds()

    def get_methods():
        """Summary

        Returns:
            TYPE: Description
        """
        if methods is not None:
            return methods

        options_resp = current_app.make_default_options_response()
        return options_resp.headers['allow']

    def decorator(f):
        """Summary

        Args:
            f (TYPE): Description

        Returns:
            TYPE: Description
        """
        def wrapped_function(*args, **kwargs):
            """Summary

            Args:
                *args: Description
                **kwargs: Description

            Returns:
                TYPE: Description
            """
            if automatic_options and request.method == 'OPTIONS':
                resp = current_app.make_default_options_response()
            else:
                resp = make_response(f(*args, **kwargs))
            if not attach_to_all and request.method != 'OPTIONS':
                return resp

            request_orign = request.environ.get('HTTP_ORIGIN', '')

            request_headers = request.environ.get('HTTP_ACCESS_CONTROL_REQUEST_HEADERS', '')

            allow_headers = request_headers if headers is None and request_headers else headers

            h = resp.headers

            h['X-Frame-Options'] = 'SAMEORIGIN'
            h['Access-Control-Allow-Origin'] = request_orign
            h['Access-Control-Allow-Methods'] = get_methods()
            h['Access-Control-Allow-Credentials'] = 'true'
            if max_age is not None:
                h['Access-Control-Max-Age'] = str(max_age)
            h['Access-Control-Allow-Headers'] = allow_headers

            return resp

        f.provide_automatic_options = False
        return update_wrapper(wrapped_function, f)
    return decorator


def login_required(f):
    @wraps(f)
    def decorator(*args, **kwargs):
        if not flask.g.user:
            return process_result(Exception('invalid user'), {}, status_code=401)

        return f(*args, **kwargs)

    return decorator


def get_user_id():
    authorization = request.headers.get('Authorization')
    if not authorization:
        return None

    prefix = 'bearer '

    if not authorization.startswith(prefix):
        return None

    authorization = authorization[len(prefix):]

    err, db_result = pyutil_mongo.db_find_one('access_token', {'access_token': authorization})
    if err:
        return None

    if not db_result:
        return None

    return db_result.get('user_id')
