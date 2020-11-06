# -*- coding: utf-8 -*-
"""Summary

Attributes:
    config (dict): Description
    logger (TYPE): Description
"""

import pyutil_cfg
from pyutil_mongo import cfg as mongo_cfg

_NAME = "openbbs_middleware"

_USER_COLLECTION_MAP = {
    'user': 'user',
    'role': 'role',
    'permission': 'permission',
}

_USER_DB_NAME = 'user'

logger = None
config = {}


def init(ini_filename, params=None):
    """init config

    Args:
        ini_filename (str): ini filename
        params (dict, optional): additional params
    """
    global logger
    global config

    logger, config = pyutil_cfg.init(_NAME, ini_filename, params=params)

    _init_mongo()


def _init_mongo():
    """Summary

    Returns:
        TYPE: Description
    """
    mongo_protocol = config.get('mongo_protocol', 'mongodb')
    hostname = ':'.join([config.get('mongo_host', 'localhost'), str(config.get('mongo_port', 27017))])
    ssl = config.get('mongo_ssl', False)
    cert = config.get('mongo_sslpemkeyfile', None)
    ca = config.get('mongo_sslca', None)

    # user-collection
    user_mongo_map = mongo_cfg.MongoMap(_USER_COLLECTION_MAP, hostname=hostname, db_name=_USER_DB_NAME, mongo_db_name=_USER_DB_NAME, ssl=ssl, cert=cert, ca=ca, mongo_protocol=mongo_protocol)

    err = mongo_cfg.init(logger, [user_mongo_map])

    return err
