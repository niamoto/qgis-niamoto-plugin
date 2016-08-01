# coding: utf-8

import os
import logging
from logging.config import dictConfig

from qgis.core import *

from niamoto_plugin.settings import LOG_PATH

# Create log file if not exists
if not os.path.isdir(LOG_PATH):
    os.makedirs(LOG_PATH)

LOGGING_CONF = {
    'version': 1,
    'formatters': {
        'f': {
            'format': '%(asctime)s %(name)-12s %(levelname)-8s %(message)s'
        }
    },
    'handlers': {
        'file': {
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': os.path.join(LOG_PATH, u"niamoto_plugin.log"),
            'level': logging.DEBUG,
            'formatter': 'f',
            'maxBytes': 1024000,
            'backupCount': 5,
        }
    },
    'root': {
        'handlers': ['file'],
        'level': logging.DEBUG,
    },
}

LOGGER = logging.getLogger()
LOGGER.setLevel(logging.DEBUG)
dictConfig(LOGGING_CONF)


def log(msg):
    QgsMessageLog.logMessage(msg, 'niamoto_plugin')
    get_logger().info(msg)


def get_logger():
    return LOGGER
