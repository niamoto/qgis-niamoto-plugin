# coding: utf-8

import os
import json
import urlparse
from collections import OrderedDict

import requests

from niamoto_plugin import DATA_PATH
from niamoto_plugin.utils import log


NIAMOTO_REST_BASE_URL = u"http://127.0.0.1:8000/api/1.0/"

DATABASE_VERSION = os.path.join(DATA_PATH, u'database_version.txt')
TAXA_TREE_PATH = os.path.join(DATA_PATH, u'taxa_tree.json')


def get_taxa_tree():
    """
    Return the cached taxa tree if it is up to date with the server one,
    else download the last one before returning it.
    :return: The taxa tree (nested).
    """
    local_version = _get_local_database_version()
    server_version = _fetch_database_server_version()
    log(u"Local taxa tree version is {}".format(local_version))
    log(u"Server taxa tree version is {}".format(server_version))
    need_download = False
    if local_version is None:
        need_download = True
    elif local_version != server_version:
            need_download = True
    if need_download:
        log(u"Downloading the taxa tree is necessary, downloading it...")
        flat_taxa_tree = _get_taxa_flat_tree_from_server()
        taxa_tree = _build_nested_tree(flat_taxa_tree)
        _write_version(server_version)
        _write_taxa_tree(taxa_tree)
        log(u"The taxa tree had been downloaded!")
        return taxa_tree
    log(u"Downloading the taxa tree is not necessary")
    return _get_local_taxa_tree()


def _fetch_database_server_version():
    """
    Fetch the niamoto rest server to get the currently active database version.
    :return: The uuid of the active database version in the server.
    """
    session = requests.Session()
    url = urlparse.urljoin(
        NIAMOTO_REST_BASE_URL,
        u"plantnote_database/?active=True"
    )
    r = session.get(url)
    db = json.loads(r.text)[0]
    return db['uuid']


def _get_local_database_version():
    """
    :return: The corresponding uuid of the database from which the local
    cached taxa tree was downloaded. None if no taxa tree is currently cached.
    """
    if not os.path.exists(DATABASE_VERSION):
        return None
    with open(DATABASE_VERSION, 'r') as version_file:
        return version_file.read()


def _write_version(version):
    with open(DATABASE_VERSION, 'w') as db_file:
        db_file.write(version)


def _write_taxa_tree(taxa_tree):
    with open(TAXA_TREE_PATH, 'w') as taxa_tree_file:
        json.dump(taxa_tree, taxa_tree_file)


def _get_local_taxa_tree():
    with open(TAXA_TREE_PATH, 'r') as taxa_tree_file:
        return json.load(taxa_tree_file)


def _get_taxa_flat_tree_from_server():
    """
    Download the currently active flat taxa tree in the niamoto server.
    :return: The flat taxa tree as an array.
    """
    flat_tree_url = NIAMOTO_REST_BASE_URL + u"taxon/"
    session = requests.Session()
    flat_tree = session.get(flat_tree_url)
    return json.loads(flat_tree.text)


def _build_nested_tree(flat_tree):
    tax_dict = OrderedDict()
    for tax in flat_tree:
        tax['children'] = list()
        tax_dict[tax['id']] = tax
    for tax in tax_dict.values():
        if tax['parent'] is not None:
            tax_dict[tax['parent']]['children'].append(tax)
    final_tax = list()
    for tax in tax_dict.values():
        if tax['parent'] is None:
            final_tax.append(tax)
    return final_tax

