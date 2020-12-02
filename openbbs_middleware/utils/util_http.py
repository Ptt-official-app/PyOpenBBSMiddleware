# -*- coding: utf-8 -*-
"""utils for http-related
"""

import re
from http.cookies import SimpleCookie

from openbbs_middleware import cfg


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
