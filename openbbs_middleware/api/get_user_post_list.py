# -*- coding: utf-8 -*-
"""Summary
"""


def get_user_post_list(user_id, params):
    '''XXX mock-data

    Args:
        username (TYPE): Description
        params (TYPE): Description

    Returns:
        TYPE: Description
    '''
    bid = 'WhoAmI'
    aid = 'aid0'

    result = {
        'list': [
            {
                'bsn': 'sn-' + bid,
                'bid': bid,
                'asn': 'sn-' + aid,
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
        'nextBID': 'WhoAmI',
        'nextAID': 'pid2',
        'nextTime': 1234567890,
    }

    return None, result
