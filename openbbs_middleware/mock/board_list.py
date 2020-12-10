# -*- coding: utf-8 -*-

from openbbs_middleware.mock.board_summary import backend_board_summary, board_summary


def backend_board_list():
    return {
        "boards": [
            backend_board_summary(),
        ],
        "next_bid": "4",
    }


def board_list():
    return {
        'list': [
            board_summary(),
        ],
        'nextIdx': '4',
    }
