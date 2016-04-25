# coding: utf-8

from collections import OrderedDict
import json

import requests


NCBIF_REST_BASE_URL = "http://127.0.0.1:8000/api/1.0/"


def fetch_taxa_flat_tree():
    flat_tree_url = NCBIF_REST_BASE_URL + "taxon/"
    session = requests.Session()
    flat_tree = session.get(flat_tree_url)
    return json.loads(flat_tree.text)


def build_nested_tree(flat_tree):
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
