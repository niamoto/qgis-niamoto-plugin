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

NIAMOTO_BASE_URL = SETTINGS.get(
    "NIAMOTO_REST_BASE_URL",
    u"https://niamoto.io/"
)
NIAMOTO_REST_BASE_URL = NIAMOTO_BASE_URL + u"api/1.0/"


def set_niamoto_base_url(value):
    global SETTINGS, \
        NIAMOTO_BASE_URL, \
        NIAMOTO_REST_BASE_URL,\
        NIAMOTO_OAUTH2_TOKEN_URL
    NIAMOTO_BASE_URL = value
    NIAMOTO_REST_BASE_URL = NIAMOTO_BASE_URL + u"api/1.0/"
    NIAMOTO_OAUTH2_TOKEN_URL = NIAMOTO_BASE_URL + u"o/token/"
    SETTINGS['NIAMOTO_BASE_URL'] = value
    write_settings()


GEOSERVER_BASE_URL = SETTINGS.get(
    "GEOSERVER_BASE_URL",
    u"https://geo.niamoto.io/geoserver/"
)


def set_geoserver_base_url(value):
    global SETTINGS,\
        GEOSERVER_BASE_URL
    GEOSERVER_BASE_URL = value
    SETTINGS['GEOSERVER_BASE_URL'] = value
    write_settings()


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

NIAMOTO_OAUTH2_TOKEN_URL = NIAMOTO_BASE_URL + u"o/token/"
OAUTH2_CLIENT_ID = SETTINGS.get(
    "OAUTH2_CLIENT_ID",
    "ystnxvD5Sjnd7UtAV3Qj3Hou8ZKAZtlzJEnHySoX"
)
OAUTH2_CLIENT_SECRET = SETTINGS.get(
    "OAUTH2_CLIENT_SECRET",
    "5HAIZVFjFF0MlK1CJE4tfHbNk734qqyxZ9XLz20ZvtQbrxd61gIhQ6FhyW0jxju26GTJtbhxJP6oTqrrV8kLcLEjW4KCmI1vBf0F6hQ2sCYnWQOAONgqoEO72w12NdKo"
)

# Create data dir if not exists
if not os.path.isdir(DATA_PATH):
    os.makedirs(DATA_PATH)
