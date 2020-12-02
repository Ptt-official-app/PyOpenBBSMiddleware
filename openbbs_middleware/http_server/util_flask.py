# -*- coding: utf-8 -*-
"""flask

Attributes:
    app (App): Flask app
    csrf (CSRF): csrf protection
    login_manager (LoginManager): Flask-Login manager
"""

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

from bson import ObjectId
import rapidjson as json

import pyutil_mongo
import traceback
from datetime import timedelta

from werkzeug.middleware.proxy_fix import ProxyFix
from openbbs_middleware import cfg

###
# customized register_user (no need to store password.)
###

app = Flask(__name__.split('.')[0])
app.wsgi_app = ProxyFix(app.wsgi_app, x_proto=1, x_host=1, x_port=1)
csrf = CSRFProtect()
csrf.init_app(app)

login_manager = flask_login.LoginManager()
login_manager.init_app(app)


def process_params():
    """Summary

    Returns:
        TYPE: Description
    """
    return None


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

    app.config.update({
        'SECRET_KEY': flask_secret_key,
        'EXPLAIN_TEMPLATE_LOADING': True,
        'MONGODB_SETTINGS': mongo_settings,
        'SESSION_PROTECTION': 'strong',
        'SECURITY_PASSWORD_HASH': 'sha512_crypt',
        'SECURITY_PASSWORD_SALT': flask_security_salt,
        'SECURITY_RECOVERABLE': False,
        'SECURITY_SEND_REGISTER_EMAIL': False,

        'SECURITY_REGISTERABLE': cfg.config.get('flask_security_registerable', True),
        'SECURITY_CONFIRMABLE': cfg.config.get('flask_security_confirmable', False),
        'SECURITY_LOGIN_URL': '/Account/login',
        'SECURITY_REGISTER_URL': '/Account/register',
        'SECURITY_LOGOUT_URL': '/Account/logout',
        'SECURITY_POST_LOGOUT_VIEW': '/Account/login',
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
    """Summary
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
        """User in flask-security. The default flask-security User information requires email and password. email and password will be removed in real development.
                https://github.com/Flask-Middleware/flask-security/blob/master/flask_security/forms.py#L355

                Attributes:
                    active (bool): active
                    jwt (str): jwt-token
                    roles (list): roles
                    user_id (str): username
        ption

        Attributes:
            active (TYPE): Description
            email (TYPE): Description
            jwt (TYPE): Description
            password (TYPE): Description
            roles (TYPE): Description
            user_id (TYPE): Description
        """

        email = StringField(max_length=1000)
        password = StringField(max_length=1000)

        user_id = StringField(max_length=1000)
        jwt = StringField(max_length=10000)
        active = BooleanField(default=True)
        roles = ListField(EmbeddedDocumentField(EmbeddedRole), default=[])

        @classmethod
        def _get_collection(cls):
            """_get_collection

            Returns:
                TYPE: user-collection from pymongo.
            """
            db = cfg.config['mongo_dbname']
            return pyutil_mongo.cfg.config[db]['db']['user']

    user_datastore = MongoEngineUserDatastore(db, User, Role)

    Security(app=app, datastore=user_datastore)
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
    def load_user(the_id):
        """Summary

        Args:
            the_id (TYPE): Description

        Returns:
            TYPE: Description
        """

        fields = ['user_id', 'jwt']
        the_id = ObjectId(the_id)
        err, db_result = pyutil_mongo.db_find('user', {})

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
