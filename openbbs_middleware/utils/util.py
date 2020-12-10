# -*- coding: utf-8 -*-


def flatten_errors(the_list_with_errs):
    the_list = [each[1] for each in the_list_with_errs]

    the_errors = [{'idx': idx, 'err': each[0]} for idx, each in enumerate(the_list_with_errs)]
    the_errors = filter(lambda x: x['err'] is not None, the_errors)
    if not the_errors:
        return None, the_list

    the_errors = list(map(lambda x: '%s:%s' % (x['idx'], x['err']), the_errors))

    return ','.join(the_errors), the_list
