# -*- coding: utf-8 -*-
"""Summary
"""

import time


def get_current_milli_ts():
    """get current milli ts

    Returns:
        TYPE: Description
    """
    return int(time.time() * 1000)


def ts_to_milli_ts(ts):
    return int(ts) * 1000
