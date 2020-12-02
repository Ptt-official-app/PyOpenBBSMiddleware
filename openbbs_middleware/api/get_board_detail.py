# -*- coding: utf-8 -*-
"""Summary
"""


def get_board_detail(bid, params):
    '''XXX mock-data

    Args:
        bid (TYPE): Description
        params (TYPE): Description

    Returns:
        TYPE: Description
    '''
    result = {
        'bsn': 'sn-%s' % (bid),
        'bid': bid,
        'title': '這是 title',
        'flag': 0,
        'boardType': 1,
        'cat': '站務',
        'onlineCount': 100000,
        'moderators': [
            {
                'usn': 'sn-teemo',
                'uid': 'teemo',
            },
            {
                'usn': 'sn-okcool',
                'uid': 'okcool',
            },
        ],
        'voteLimitLogins': 10,
        'bUpdate': 1234567890,
        'postLimitLogins': 10,
        'vote': 3,
        'vtime': 1234567890,
        'level': 123,
        'lastSetTime': 1234567890,
        'postExpire': 120,
        'endGamble': 1234567890,
        'postType': 'post-type',
        'fastRecommendPause': 60,
        'voteLimitBadpost': 15,
        'postLimitBadpost': 13,
        'read': False,
    }

    return None, result
