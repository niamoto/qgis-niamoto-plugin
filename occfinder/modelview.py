# coding: utf-8

import re

from PyQt4.QtCore import *


LEVEL_LABELS = {
    'FAMILY': u'Famille',
    'GENUS': u'Genre',
    'SPECIE': u'Espèce',
    'INFRA': u'Infra',
}


class TaxonNode(object):

    def __init__(self, taxon_dict, parent=None, match_pattern=''):
        self.id = taxon_dict['id']
        self.full_name = taxon_dict['full_name']
        self.level_name = taxon_dict['level_name']
        self.level = taxon_dict['level']
        self.parent = parent
        self.match_pattern = re.compile(".*{}.*".format(match_pattern))
        match = self.match_pattern.match(self.full_name.lower())
        self.matching = match is not None
        self.children = list()
        children = taxon_dict.get('children', None)
        if children is None:
            pass
        else:
            for c in children:
                node = TaxonNode(c, self, match_pattern)
                self.children.append(node)
        self.matching_children = self.find_matching_children()

    def has_matching_child(self):
        """
        :return: True if the node or one of its children is matching the
        matching pattern.
        """
        if self.matching:
            return True
        for c in self.children:
            if c.matching:
                return True
            if c.has_matching_child():
                return True
        return False

    def find_matching_children(self):
        return [c for c in self.children if c.has_matching_child()]

    def update_matching(self, match_pattern=''):
        self.match_pattern = re.compile(".*{}.*".format(match_pattern))
        match = self.match_pattern.match(self.full_name.lower())
        self.matching = match is not None
        for c in self.children:
            c.update_matching(match_pattern)
        self.matching_children = self.find_matching_children()


class TaxonTreeItemModel(QAbstractItemModel):

    HEADERS = ["Nom complet du taxon", "Niveau"]

    def __init__(self, root_items=None, match_pattern=''):
        super(TaxonTreeItemModel, self).__init__()
        self.root_nodes = None
        self.matching_root_nodes = None
        self.match_pattern = match_pattern
        self.reset_taxon_tree(root_items)
        self.headerDataChanged.emit(Qt.Horizontal, 0, 1)

    def reset_taxon_tree(self, root_items):
        self.beginResetModel()
        self.root_nodes = None
        self.matching_root_nodes = None
        if root_items is not None and len(root_items) > 0:
            self.root_nodes = [TaxonNode(t, None, self.match_pattern)
                               for t in root_items]
            self.matching_root_nodes = self.find_matching_root_nodes()
        self.endResetModel()

    def update_match_pattern(self, match_pattern=''):
        self.beginResetModel()
        for node in self.root_nodes:
            node.update_matching(match_pattern)
            self.matching_root_nodes = self.find_matching_root_nodes()
        self.endResetModel()

    def find_matching_root_nodes(self):
        return [n for n in self.root_nodes if n.has_matching_child()]

    def columnCount(self, parent):
        return 2

    def rowCount(self, parent):
        if self.matching_root_nodes is None:
            return 0
        if not parent.isValid():
            return len(self.matching_root_nodes)
        return len(parent.internalPointer().matching_children)

    def hasChildren(self, parent):
        return self.rowCount(parent) > 0

    def index(self, row, column, parent=QModelIndex()):
        if not parent.isValid():
            return self.createIndex(row, column, self.matching_root_nodes[row])
        if row >= self.rowCount(parent):
            return QModelIndex()
        else:
            parent_node = parent.internalPointer()
            return self.createIndex(
                row,
                column,
                parent_node.matching_children[row]
            )

    def parent(self, index):
        if not index.isValid():
            return QModelIndex()
        node = index.internalPointer()
        if node.parent is None:
            return QModelIndex()
        else:
            row = node.parent.matching_children.index(node)
            return self.createIndex(row, 0, node.parent)

    def data(self, index, role):
        if not index.isValid():
            return None
        node = index.internalPointer()
        if role == Qt.DisplayRole and index.column() == 0:
            return node.full_name
        if role == Qt.DisplayRole and index.column() == 1:
            return LEVEL_LABELS[node.level]
        return None

    def headerData(self, section, orientation, role=Qt.DisplayRole):
        if orientation == Qt.Horizontal and role == Qt.DisplayRole:
            return self.HEADERS[section]
        if role == Qt.TextAlignmentRole:
            return Qt.AlignCenter
        return None
