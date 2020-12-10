# -*- coding: utf-8 -*-


def _int(x):
    try:
        result = int(x)
        return None, result
    except Exception as e:
        return e, 0
