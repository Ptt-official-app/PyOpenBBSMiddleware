# -*- coding: utf-8 -*-

import unittest
import logging

from openbbs_middleware.utils import util_http


class TestUtilHttp(unittest.TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_parse_cookies(self):
        cookie_str = 'session=eyJjc3JmX3Rva2VuIjoiMmE1MDE0NTU3ZjFlNTg5NjAyMzE5MGI4YTZiM2ZjMWUwZjBlYTVlMiJ9.X8awlA.qXWBN_UJ9ZaHU0i3NwXd3lga-8s;'

        cookies = util_http.parse_cookies([cookie_str])

        logging.info('cookies: %s', cookies)

        self.assertEqual(cookies['session'], 'eyJjc3JmX3Rva2VuIjoiMmE1MDE0NTU3ZjFlNTg5NjAyMzE5MGI4YTZiM2ZjMWUwZjBlYTVlMiJ9.X8awlA.qXWBN_UJ9ZaHU0i3NwXd3lga-8s')

    def test_util_http(self):
        text = """
<form action="/Account/login" method="POST" name="login_user_form">
  <input id="next" name="next" type="hidden" value="">
<input id="csrf_token" name="csrf_token" type="hidden" value="ImMyYjM4MGZlYjVmOTY0ZGI2MTEyNzQ1ZGNjNzk2MWM0YzViYzFlNzUi.X8azqQ.0R0rIgbGzCrpsoHcvB6I4I62gZg">

  <p>
    <label for="email">Email Address</label> <input id="email" name="email" required type="text" value="">
"""
        csrf_token = util_http.parse_csrftoken(text)

        self.assertEqual(csrf_token, 'ImMyYjM4MGZlYjVmOTY0ZGI2MTEyNzQ1ZGNjNzk2MWM0YzViYzFlNzUi.X8azqQ.0R0rIgbGzCrpsoHcvB6I4I62gZg')
