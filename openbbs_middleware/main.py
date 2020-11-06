#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""main
"""

import gevent.monkey
gevent.monkey.patch_all()

import argparse

import flask
import flask_login
from flask import send_from_directory, jsonify

from gevent.pywsgi import WSGIServer
from flask_swagger import swagger

from openbbs_middleware import cfg
from openbbs_middleware.utils import util_flask
from openbbs_middleware.utils.util_flask import app, csrf


@app.before_request
def before_request():
    """before-request
    """
    flask.g.user = flask_login.current_user


@app.route('/')
def index():
    """
    swagger_from_file: apidoc/index.yaml
    """
    return util_flask.process_result(None, {'index': ''})


@app.route('/spec')
@csrf.exempt
def spec():
    """spec
    """
    swag = swagger(app, from_file_keyword='swagger_from_file')
    return jsonify(swag)


@app.route('/<path:path>')
def send_root_path(path):
    """static files.
    """
    return send_from_directory(app.static_folder, path)


def parse_args():
    """
    parse args

    Returns:
        args: args
    """
    parser = argparse.ArgumentParser(description='opebbs-middleware')
    parser.add_argument('-i', '--ini', type=str, required=True, help="ini filename")
    parser.add_argument('--host', default='127.0.0.1', type=str)
    parser.add_argument('-p', '--port', type=int, required=True, help="port")

    args = parser.parse_args()

    return args


def _init():
    """init
    """
    args = parse_args()
    cfg.init(args.ini, {'port': args.port})
    util_flask.init_flask()

    return args


if __name__ == '__main__':
    args = _init()

    cfg.logger.info('to run server')
    http_server = WSGIServer((args.host, args.port), app)
    http_server.serve_forever()
