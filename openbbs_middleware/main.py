#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""main
"""

import gevent.monkey
gevent.monkey.patch_all()

import argparse

import rapidjson as json

import flask
import flask_login
from flask import send_from_directory, jsonify
from flask_security import login_required
from flask_security import views

from gevent.pywsgi import WSGIServer
from flask_swagger import swagger

from openbbs_middleware import cfg
from openbbs_middleware.http_server import util_flask
from openbbs_middleware.http_server.util_flask import app, crossdomain

_APP_PREFIX = '/api'


def _with_app_prefix(path):
    """Summary

    Args:
        path (TYPE): Description

    Returns:
        TYPE: Description
    """
    if not _APP_PREFIX:
        return path
    return _APP_PREFIX + path


with open('apidoc/template.json', 'r') as f:
    template = json.load(f)


@app.before_request
def before_request():
    """before-request
    """
    flask.g.user = flask_login.current_user


@app.route('/')
@login_required
def _index():
    """
    swagger_from_file: apidoc/index.yaml

    Returns:
        TYPE: Description
    """
    return util_flask.process_result(None, {'index': ''})


@app.route('/spec')
@crossdomain()
def spec():
    """
    Returns:
        TYPE: Description
    """

    swag = swagger(app, from_file_keyword='swagger_from_file', template=template)
    return jsonify(swag)


from openbbs_middleware.api.get_popular_post import get_popular_post
@app.route(_with_app_prefix('/Article/populars'))
@crossdomain()
def _get_popular_post():
    """
    swagger_from_file: apidoc/get_popular_post.yaml

    Returns:
        TYPE: Description
    """
    params = util_flask.process_params()
    err, result = get_popular_post(params)
    return util_flask.process_result(err, result)


from openbbs_middleware.api.get_favorite_board import get_favorite_board
@app.route(_with_app_prefix('/Board/favorite/<username>'))
@crossdomain()
def _get_favorite_board(username):
    """
    swagger_from_file: apidoc/get_favorite_board.yaml

    Args:
        username (TYPE): Description

    Returns:
        TYPE: Description
    """
    params = util_flask.process_params()
    err, result = get_favorite_board(username, params)
    return util_flask.process_result(err, result)


from openbbs_middleware.api.find_board_by_name import find_board_by_name
@app.route(_with_app_prefix('/Board/search'))
@crossdomain()
def _find_board_by_name():
    """
    swagger_from_file: apidoc/find_board_by_name.yaml

    Returns:
        TYPE: Description
    """
    params = util_flask.process_params()
    err, result = find_board_by_name(params)
    return util_flask.process_result(err, result)


from openbbs_middleware.api.get_popular_board_list import get_popular_board_list
@app.route(_with_app_prefix('/Board/populars'))
@crossdomain()
def _get_popular_board_list():
    """
    swagger_from_file: apidoc/get_popular_board_list.yaml

    Returns:
        TYPE: Description
    """
    params = util_flask.process_params()
    err, result = get_popular_board_list(params)
    return util_flask.process_result(err, result)


from openbbs_middleware.api.get_user_info import get_user_info
@app.route(_with_app_prefix('/User/Users/<username>'))
@crossdomain()
def _get_user_info(username):
    """
    swagger_from_file: apidoc/get_user_info.yaml

    Args:
        username (TYPE): Description

    Returns:
        TYPE: Description
    """
    params = util_flask.process_params()
    err, result = get_user_info(username, params)
    return util_flask.process_result(err, result)


from openbbs_middleware.api.get_user_post_list import get_user_post_list
@app.route(_with_app_prefix('/User/Article/<username>'))
@crossdomain()
def _get_user_post_list(username):
    """
    swagger_from_file: apidoc/get_user_post_list.yaml

    Args:
        username (TYPE): Description

    Returns:
        TYPE: Description
    """
    params = util_flask.process_params()
    err, result = get_user_post_list(username, params)
    return util_flask.process_result(err, result)


from openbbs_middleware.api.get_user_comment_list import get_user_comment_list
@app.route(_with_app_prefix('/User/Comment/<username>'))
@crossdomain()
def _get_user_comment_list(username):
    """
    swagger_from_file: apidoc/get_user_comment_list.yaml

    Args:
        username (TYPE): Description

    Returns:
        TYPE: Description
    """
    params = util_flask.process_params()
    err, result = get_user_comment_list(username, params)
    return util_flask.process_result(err, result)


from openbbs_middleware.api.get_post_list import get_post_list
@app.route(_with_app_prefix('/Article/Articles/<board>'))
@crossdomain()
def _get_post_list(board):
    """
    swagger_from_file: apidoc/get_post_list.yaml

    Args:
        board (TYPE): Description

    Returns:
        TYPE: Description
    """
    params = util_flask.process_params()
    err, result = get_post_list(board, params)
    return util_flask.process_result(err, result)


from openbbs_middleware.api.get_post import get_post
@app.route(_with_app_prefix('/Article/Articles/<board>/<article>'))
@crossdomain()
def _get_post(board, article):
    """
    swagger_from_file: apidoc/get_post.yaml

    Args:
        board (TYPE): Description
        article (TYPE): Description

    Returns:
        TYPE: Description
    """
    params = util_flask.process_params()
    err, result = get_post(board, article, params)
    return util_flask.process_result(err, result)


from openbbs_middleware.api.get_board_detail import get_board_detail
@app.route(_with_app_prefix('/Board/Boards/<board>'))
@crossdomain()
def _get_board_detail(board):
    """
    swagger_from_file: apidoc/get_board_detail.yaml

    Args:
        board (TYPE): Description

    Returns:
        TYPE: Description
    """
    params = util_flask.process_params()
    err, result = get_board_detail(board, params)
    return util_flask.process_result(err, result)


from openbbs_middleware.api.get_board_title import get_board_title
@app.route(_with_app_prefix('/Board/Title/<board>'))
@crossdomain()
def _get_board_title(board):
    """
    swagger_from_file: apidoc/get_board_title.yaml

    Args:
        board (TYPE): Description

    Returns:
        TYPE: Description
    """
    params = util_flask.process_params()
    err, result = get_board_title(board, params)
    return util_flask.process_result(err, result)


@app.route('/<path:path>')
def send_root_path(path):
    """static files.

    Args:
        path (TYPE): Description

    Returns:
        TYPE: Description
    """
    try:
        return send_from_directory(app.static_folder, path)
    except:
        return '', 404, None


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

    Returns:
        TYPE: Description
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
