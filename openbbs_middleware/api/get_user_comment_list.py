# -*- coding: utf-8 -*-
"""Summary
"""


def get_user_comment_list(user_id, params):
    '''XXX mock-data

    Args:
        username (TYPE): Description
        params (TYPE): Description

    Returns:
        TYPE: Description
    '''
    result = {
        'list': [
            {
                'bsn': 'sn-SYSOP',
                'bid': 'SYSOP',
                'asn': 'sn-aid2',
                'aid': 'aid2',
                'csn': 'sn-cid3',
                'cid': 'cid3',
                'postTime': 1234567891,
                'title': '[公告] 你誰啊, 亂公告',
                'comment': '我是站長',
                'flag': 0,
            },
        ],
        'nextBID': 'Joke',
        'nextAID': 'aid1',
        'nextCID': 'cid2',
        'nextTime': 1234567890,
    }

    return None, result
