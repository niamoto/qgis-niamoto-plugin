# coding: utf-8

import urllib

from PyQt4.QtCore import *
from PyQt4.QtGui import *
from qgis.core import *

from niamoto_plugin.fetch_data import get_taxa_tree
from niamoto_plugin.modelview import TaxonTreeItemModel
from niamoto_plugin.ui.taxon_dock import Ui_TaxonTreeWidget
from utils import log


GEOSERVER_BASE_URL = "http://localhost:8080/geoserver"


class NiamotoPlugin(object):

    def __init__(self, iface):
        self.iface = iface
        self.taxon_dock = QDockWidget("niamoto_plugin")
        self.taxon_tree_widget = TaxonTreeWidget(self.iface)
        self.taxon_dock.setWidget(self.taxon_tree_widget)

    def initGui(self):
        self.iface.addDockWidget(Qt.RightDockWidgetArea, self.taxon_dock)

    def run(self):
        self.taxon_dock.show()

    def unload(self):
        pass


class TaxonTreeWidget(QWidget, Ui_TaxonTreeWidget):

    def __init__(self, iface, parent=None):
        super(TaxonTreeWidget, self).__init__(parent)
        self.setupUi(self)
        self.iface = iface
        log("Loading taxon tree...")
        root_items = get_taxa_tree()
        self.taxon_tree_model = TaxonTreeItemModel(root_items)
        self.taxon_treeview.setModel(self.taxon_tree_model)
        self.filter_button.clicked.connect(self.change_pattern)
        self.taxon_treeview.expandAll()
        for i in range(self.taxon_tree_model.columnCount(None)):
            self.taxon_treeview.resizeColumnToContents(i)
        selection_model = self.taxon_treeview.selectionModel()
        selection_model.currentChanged.connect(self.current_taxon_changed)
        self.wfs_button.clicked.connect(self.add_wfs_layer)
        self.all_occurrences_button.clicked \
            .connect(self.add_wfs_layer_all_taxons)
        self.expand_button.clicked.connect(self.taxon_treeview.expandAll)
        self.collapse_button.clicked.connect(self.taxon_treeview.collapseAll)
        self.current_taxon_changed()

    def change_pattern(self):
        pattern = self.filter_edit.text()
        self.taxon_tree_model.update_match_pattern(pattern)
        self.taxon_treeview.expandAll()

    @property
    def current_taxon(self):
        """
        :return: The current selected taxon, None if none is selected.
        """
        index = self.taxon_treeview.currentIndex()
        if index.isValid():
            taxon = index.internalPointer()
            return taxon
        return None

    def current_taxon_changed(self):
        if self.current_taxon is None:
            self.taxon_label.setText("")
            self.wfs_button.setEnabled(False)
        else:
            self.taxon_label.setText(self.current_taxon.full_name)
            self.wfs_button.setEnabled(True)

    def add_wfs_layer(self):
        log("Adding wfs layer for taxon {}"
            .format(self.current_taxon.full_name))
        uri = self.get_wfs_uri()
        log(uri)
        vlayer = QgsVectorLayer(uri, self.current_taxon.full_name, "WFS")
        QgsMapLayerRegistry.instance().addMapLayer(vlayer)

    def add_wfs_layer_all_taxons(self):
        log("Adding wfs layer for all taxons"
            .format(self.current_taxon.full_name))
        params = {
            'service': 'WFS',
            'version': '1.0.0',
            'request': 'GetFeature',
            'srsname': 'EPSG:4326',
            'typename': 'pn_forests_portal:occurrences_for_taxon',
        }
        uri = GEOSERVER_BASE_URL + '/wfs?' \
            + urllib.unquote(urllib.urlencode(params))
        log(uri)
        vlayer = QgsVectorLayer(uri, "Toutes les occurrences", "WFS")
        QgsMapLayerRegistry.instance().addMapLayer(vlayer)

    def get_wfs_uri(self):
        params = {
            'service': 'WFS',
            'version': '1.0.0',
            'request': 'GetFeature',
            'srsname': 'EPSG:4326',
            'typename': 'pn_forests_portal:occurrences_for_taxon',
            'viewparams': 'id_taxon:{}'.format(self.current_taxon.id),
        }
        uri = GEOSERVER_BASE_URL + '/wfs?' \
            + urllib.unquote(urllib.urlencode(params))
        return uri
