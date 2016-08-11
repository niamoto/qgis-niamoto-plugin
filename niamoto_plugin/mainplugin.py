# coding: utf-8

import urllib

from PyQt4.QtCore import *
from PyQt4.QtGui import *
from qgis.core import *
from requests import ConnectionError

from niamoto_plugin.fetch_data import get_taxa_tree
from niamoto_plugin.modelview import TaxonTreeItemModel
from niamoto_plugin.ui.taxon_dock import Ui_TaxonTreeWidget
from niamoto_plugin import settings
from utils import log, construct_wfs_uri


NIAMOTO_WFS_URL = settings.GEOSERVER_BASE_URL + '/wfs'


class NiamotoPlugin(object):

    CONNECTION_FAILED_TEXT = \
        u"""
        Ahou pardon! La connection au serveur a échoué, vérifiez votre,
        connection internet. Si malgré ça le problème persiste, contactez les
        développeurs de niamoto.
        """
    RETRY_CONNECTION_TEXT = u"Retenter la connection"

    def __init__(self, iface):
        self.iface = iface
        self.taxon_dock = QDockWidget("Niamoto Plugin")
        self.taxon_tree_widget = None
        self.connection_failed_widget = None
        self.retry_button = None
        self.init_connection_failed_widget()
        self.init_taxon_widget()

    def init_taxon_widget(self):
        try:
            self.retry_button.setEnabled(False)
            self.taxon_tree_widget = TaxonTreeWidget(self.iface)
            self.taxon_dock.setWidget(self.taxon_tree_widget)
        except (ConnectionError, Exception):
            log(u"Connection failed!")
            self.retry_button.setEnabled(True)
            self.taxon_dock.setWidget(self.connection_failed_widget)

    def init_connection_failed_widget(self):
        label = QLabel(self.CONNECTION_FAILED_TEXT)
        self.retry_button = QPushButton(self.RETRY_CONNECTION_TEXT)
        self.retry_button.clicked.connect(self.init_taxon_widget)
        layout = QVBoxLayout()
        spacer = QSpacerItem(
            10, 10,
            QSizePolicy.MinimumExpanding,
            QSizePolicy.Expanding
        )
        layout.addItem(spacer)
        layout.addWidget(label)
        layout.addWidget(self.retry_button)
        layout.addItem(QSpacerItem(spacer))
        self.connection_failed_widget = QWidget()
        self.connection_failed_widget.setLayout(layout)

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
        self.taxon_treeview.doubleClicked.connect(self.add_wfs_layer)
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
        log("Adding wfs layer for all taxons")
        uri = construct_wfs_uri(
            NIAMOTO_WFS_URL,
            'niamoto:occurrence_taxon_descendants',
            version='1.0.0',
            srsname='EPSG:4326',
        )
        log(uri)
        vlayer = QgsVectorLayer(uri, "Toutes les occurrences", "WFS")
        QgsMapLayerRegistry.instance().addMapLayer(vlayer)

    def get_wfs_uri(self):
        view_params = '?viewparams=id_taxon:{}'.format(self.current_taxon.id)
        uri = construct_wfs_uri(
            NIAMOTO_WFS_URL + view_params,
            'niamoto:occurrence_taxon_descendants',
            version='1.0.0',
            srsname='EPSG:4326',
        )
        log(uri)
        return uri
