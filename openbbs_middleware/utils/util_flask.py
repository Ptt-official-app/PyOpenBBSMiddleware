# -*- coding: utf-8 -*-
"""flask

Attributes:
    app (App): Flask app
    csrf (CSRF): csrf protection
    login_manager (LoginManager): Flask-Login manager
"""


from bson.objectid import ObjectId
import pyutil_json as json

import flask
from flask import Flask

import flask_login
from flask.json import jsonify

from flask_mongoengine import MongoEngine
from flask_security import Security, MongoEngineUserDatastore, UserMixin, RoleMixin
from flask_mail import Mail

from flask_wtf.csrf import CSRFProtect

from mongoengine import StringField, ListField, BooleanField, DateTimeField, EmbeddedDocumentField, EmbeddedDocument

from werkzeug.middleware.proxy_fix import ProxyFix
from openbbs_middleware import cfg
from openbbs_middleware.cfg import _USER_DB_NAME
import pyutil_mongo
import traceback

app = Flask(__name__.split('.')[0])
app.wsgi_app = ProxyFix(app.wsgi_app, x_proto=1, x_host=1, x_port=1)
csrf = CSRFProtect()
csrf.init_app(app)

login_manager = flask_login.LoginManager()
login_manager.init_app(app)


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
        http_result = {'success': False, 'err': str(err)}
    else:
        http_result = {'success': True, 'data': the_dict}

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
    host = '%s://%s:%s' % (mongo_protocol, mongo_host, mongo_port)

    mongo_settings = {
        'db': _USER_DB_NAME,
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

    app.config.update({
        'SECRET_KEY': flask_secret_key,
        'MONGODB_SETTINGS': mongo_settings,
        'SESSION_PROTECTION': 'strong',
        'SECURITY_PASSWORD_HASH': 'sha512_crypt',
        'SECURITY_PASSWORD_SALT': flask_security_salt,
        'SECURITY_RECOVERABLE': True,
        'SECURITY_REGISTERABLE': cfg.config.get('flask_security_registerable', True),
        'SECURITY_CONFIRMABLE': cfg.config.get('flask_security_confirmable', True),
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
    })

    app.static_folder = cfg.config.get('flask_static_folder', None)


def _init_db():
    """Summary
    """
    db = MongoEngine(app)

    class Role(db.Document, RoleMixin):
        """Summary

        Attributes:
            description (TYPE): Description
            name (TYPE): Description
        """

        name = StringField(max_length=80, unique=True)
        description = StringField(max_length=255)

    class EmbeddedRole(EmbeddedDocument, RoleMixin):
        """Summary

        Attributes:
            description (TYPE): Description
            name (TYPE): Description
            permissions (TYPE): Description
        """

        name = StringField(max_length=80)
        description = StringField(max_length=255)
        permissions = StringField()

    class User(db.Document, UserMixin):
        """Summary

        Attributes:
            active (TYPE): Description
            confirmed_at (TYPE): Description
            email (TYPE): Description
            emails (TYPE): Description
            nickname (TYPE): Description
            password (TYPE): Description
            roles (TYPE): Description
            username (TYPE): Description
        """

        username = StringField(max_length=1000)
        nickname = StringField(max_length=1000)
        email = StringField(max_length=255)
        emails = ListField(StringField(max_length=255), default=[])
        password = StringField(max_length=255)
        active = BooleanField(default=True)
        confirmed_at = DateTimeField()
        roles = ListField(EmbeddedDocumentField(EmbeddedRole), default=[])

    user_datastore = MongoEngineUserDatastore(db, User, Role)
    Security(app, user_datastore)
    Mail(app)

    @app.login_manager.unauthorized_handler
    def unauth_handler():
        """Summary

        Returns:
            TYPE: Description
        """
        return jsonify(success=False,
                       data={'login_required': True},
                       message='Authorize please to access this page'), 401

    @app.login_manager.user_loader
    def load_user(user_id):
        """Summary

        Args:
            user_id (TYPE): Description

        Returns:
            TYPE: Description
        """
        try:
            fields = {
                'email': True,
                'first_name': True,
                'last_name': True,
            }

            the_id = ObjectId(user_id)

            error, db_result = pyutil_mongo.db_find_one('user', {'_id': the_id}, fields, db_name=_USER_DB_NAME)

            if error:
                cfg.logger.error('unable to find user: e: %s', error)
                return
            if not db_result:
                cfg.logger.error('user not exist')
                return

            username = db_result.get('username', '')
            nickname = db_result.get('nickname', '')
            email = db_result.get('email', '')

            return User(username=username, nickname=nickname, email=email)

        except (TypeError, ValueError) as e:
            cfg.logger.error('unable to get user_id: user_id: %s e: %s', user_id, e)
            traceback.print_stack(e)
