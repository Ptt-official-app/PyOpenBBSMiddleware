# -*- coding: utf-8 -*-
"""Summary
"""


def get_favorite_board(user_id, params):
    '''XXX mock-data

    Args:
        user_id (TYPE): Description
        params (TYPE): Description

    Returns:
        TYPE: Description
    '''
    result = {
        'list': [
            {
                'bsn': 'sn-PttNewhand',
                'bid': 'PttNewhand',
                'title': '批踢踢新手客服中心… 〃非test板',
                'flag': 1,
                'boardType': 2,
                'cat': '新手',
                'onlineCount': 100,
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
                'read': False,
            },
        ],
        'nextBID': '',
    }
    return None, result
