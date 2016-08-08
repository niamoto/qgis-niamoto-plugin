# coding: utf-8

import os
import logging
from logging.handlers import RotatingFileHandler

from qgis.core import *

from niamoto_plugin.settings import LOG_PATH

# Create log file if not exists
if not os.path.isdir(LOG_PATH):
    os.makedirs(LOG_PATH)

FORMATTER = logging.Formatter(
    '%(asctime)s %(name)-12s %(levelname)-8s %(message)s')
HANDLER = RotatingFileHandler(
    os.path.join(LOG_PATH, u"niamoto_plugin.log"),
    'a',
    1024000,
    5
)
HANDLER.setFormatter(FORMATTER)
HANDLER.setLevel(logging.DEBUG)

LOGGER = logging.getLogger()
LOGGER.setLevel(logging.DEBUG)
LOGGER.addHandler(HANDLER)


def log(msg):
    QgsMessageLog.logMessage(msg, 'niamoto_plugin')
    get_logger().info(msg)


def get_logger():
    return LOGGER


def construct_wfs_uri(url, typename, **kwargs):
    params = {
        'url': url,
        'typename': typename
    }
    params.update(kwargs)
    return ' '.join(['{}="{}"'.format(k, v) for k, v in params.items()])
