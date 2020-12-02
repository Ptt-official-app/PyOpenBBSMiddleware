# -*- coding: utf-8 -*-
"""Summary
"""


def get_post(bid, aid, params):
    '''XXX mock-data

    Args:
        bid (TYPE): Description
        aid (TYPE): Description
        params (TYPE): Description

    Returns:
        TYPE: Description
    '''
    result = {
        'bsn': 'sn-%s' % (bid),
        'bid': bid,
        'asn': 'sn-%s' % (aid),
        'aid': aid,
        'postTime': 1234567890,
        'updateTime': 1234567890,
        'date': '2009-12-14',
        'title': '天天晴人節',
        'href': '/Article/%s/%s' % (bid, aid),
        'authorsn': 'sn-teemo',
        'author': 'teemo',
        'main': '天氣晴',
        'content': ['天氣晴', '噓 okcool: 真的嗎？～'],
        'read': False,
        'flag': 0,
        'cat': '心情',
        'money': 1,
        'nReader': 1000,
        'nRecommend': -1000,
    }

    return None, result
