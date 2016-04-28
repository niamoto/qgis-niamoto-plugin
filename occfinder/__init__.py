# coding: utf-8

import os


PACKAGE_ROOT = os.path.abspath(os.path.dirname(__file__))

DATA_PATH = os.path.join(PACKAGE_ROOT, u"data")


def classFactory(iface):
    from mainplugin import OccFinder
    return OccFinder(iface)
