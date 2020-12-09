# -*- coding: utf-8 -*-
"""utils for http-related
"""

import re
from http.cookies import SimpleCookie

from openbbs_middleware import cfg
import rapidjson as json
import requests

from flask import request


def parse_cookies(cookie_list):
    """parse cookies

    Args:
        cookie_list (TYPE): a list of cookies

    Returns:
        dict: cookies
    """
    cookies = {}
    for each in cookie_list:
        each_cookie = parse_cookie_str(each)
        cookies.update(each_cookie)

    return cookies


def parse_cookie_str(cookie_str):
    """parse cookie-str

    Args:
        cookie_str (str): cookie-string

    Returns:
        dict: cookies
    """
    cookie = SimpleCookie()
    cookie.load(cookie_str)
    cookies = {key: morsal.value for key, morsal in cookie.items()}

    return cookies


def parse_csrftoken(text):
    """parse csrftoken from html-context. currently used in tests.

    Args:
        text (str): html-content

    Returns:
        str: csrf-token.
    """
    the_match = re.search(r'csrf_token.*?value="(.*?)"', text, re.M | re.S)
    if the_match:
        return the_match.group(1)

    return ''


def http_post(url, data=None, is_json=True, headers=None):
    """htt-post

    Args:
        url (str): Description
        data (dict, optional): Description
        is_json (bool, optional): Description

    Returns:
        TYPE: Description
    """
    if is_json and type(data) == dict:
        data = json.dumps(data)

    if headers is None:
        headers = {}

    remote_addr = request.remote_addr
    host = cfg.config.get('host', '')

    headers['Host'] = host
    headers['X-Forwarded-For'] = remote_addr

    authorization = request.headers.get('Authorization')
    if authorization:
        headers['Authorization'] = authorization

    r = requests.post(url, data=data, headers=headers)

    if r.status_code != 200:
        return Exception('status_code: %s' % (r.status_code)), {'err': r.text}

    try:
        the_struct = r.json()
    except Exception as e:
        return e, {}

    return None, the_struct
