# coding: utf-8

import os
import json

from niamoto_plugin import PACKAGE_ROOT


SETTINGS_FILE = os.path.join(PACKAGE_ROOT, "settings.json")
SETTINGS = dict()


def load_settings():
    global SETTINGS
    with open(SETTINGS_FILE, 'r') as settings_file:
        SETTINGS = json.load(settings_file)


def write_settings():
    with open(SETTINGS_FILE, 'w') as settings_file:
        json.dump(SETTINGS, settings_file)


load_settings()


DATA_PATH = SETTINGS.get(
    "DATA_PATH",
    os.path.join(PACKAGE_ROOT, u"data")
)

NIAMOTO_REST_BASE_URL = SETTINGS.get(
    "NIAMOTO_REST_BASE_URL",
    u"http://niamoto.ird.nc/api/1.0/"
)

GEOSERVER_BASE_URL = SETTINGS.get(
    "GEOSERVER_BASE_URL",
    u"http://geoniamoto.ird.nc/geoserver/niamoto"
)

DATABASE_VERSION_PATH = SETTINGS.get(
    "DATABASE_VERSION_PATH",
    os.path.join(DATA_PATH, u'database_version.txt')
)

TAXA_TREE_PATH = SETTINGS.get(
    "TAXA_TREE_PATH",
    os.path.join(DATA_PATH, u'taxa_tree.json')
)

LOG_PATH = SETTINGS.get(
    "LOG_PATH",
    os.path.join(PACKAGE_ROOT, u"log")
)

# Create data dir if not exists
if not os.path.isdir(DATA_PATH):
    os.makedirs(DATA_PATH)
