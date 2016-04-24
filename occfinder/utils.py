# coding: utf-8

from qgis.core import *


def log(msg):
    QgsMessageLog.logMessage(msg, 'occfinder')
