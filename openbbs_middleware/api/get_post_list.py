# -*- coding: utf-8 -*-
"""Summary
"""


def get_post_list(bid, params):
    '''XXX mock-data

    Args:
        bid (TYPE): Description
        params (TYPE): Description

    Returns:
        TYPE: Description
    '''
    aid = 'aid0'
    result = {
        'list': [
            {
                'bsn': 'sn-' + bid,
                'bid': bid,
                'aid': aid,
                'aid': aid,
                'postTime': 1234567891,
                'updateTime': 1234567891,
                'date': '2009-02-14',
                'title': '我在哪裡？',
                'href': '/Article/%s/%s' % (bid, aid),
                'authorsn': 'sn-teemo',
                'author': 'teemo',
                'read': False,
                'flag': 0,
                'cat': '問題',
                'money': 1,
                'nReader': 1,
                'nRecommend': -1000,
            },
        ],
        'nextAID': 'aid1',
        'nextTime': 1234567890,
    }

    return None, result
