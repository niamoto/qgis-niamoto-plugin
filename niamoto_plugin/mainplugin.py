# coding: utf-8

import json

from PyQt4.QtCore import *
from PyQt4.QtGui import *
from qgis.core import *
import requests
from requests import ConnectionError

from niamoto_plugin.fetch_data import get_taxa_tree
from niamoto_plugin.modelview import TaxonTreeItemModel
from niamoto_plugin.ui.taxon_dock import Ui_TaxonTreeWidget
from niamoto_plugin import settings
from ui.authentication_widget import Ui_AuthenticationWidget
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
        self.authentication_widget = None
        self.retry_button = None
        self.session = None
        self.init_authentication_widget()
        self.init_connection_failed_widget()
        self.authenticate()

    def authenticate(self):
        self.authentication_widget.status_label.setText(u"")
        if self.session is None:
            self.authentication_widget.login_edit.setText(u"")
            self.authentication_widget.password_edit.setText(u"")
            self.taxon_dock.setWidget(self.authentication_widget)
        else:
            self.connect()

    def connect(self):
        username = self.authentication_widget.login_edit.text()
        password = self.authentication_widget.password_edit.text()
        if not username or not password:
            t = u"Les informations de connexion sont incorrectes."
            st = u"color: red;"
            self.authentication_widget.status_label.setStyleSheet(st)
            self.authentication_widget.status_label.setText(t)
            self.session = None
            return
        try:
            data = {
                u"grant_type": u"password",
                u"username": username,
                u"password": password,
            }
            auth = (settings.OAUTH2_CLIENT_ID, settings.OAUTH2_CLIENT_SECRET)
            r = requests.post(
                settings.NIAMOTO_OAUTH2_TOKEN_URL,
                data=data, auth=auth
            )
            if r.status_code == requests.codes.ok:
                token = json.loads(r.text)
                self.session = {
                    u"token_type": token[u"token_type"],
                    u"access_token": token[u"access_token"],
                    u"refresh_token": token[u"refresh_token"]
                }
                self.get_whoami()
                t = u"Authentification réussie, chargement des données..."
                st = u"color: green;"
                self.authentication_widget.status_label.setStyleSheet(st)
                self.authentication_widget.status_label.setText(t)
                QApplication.processEvents()
                self.init_taxon_widget()
            elif r.status_code == requests.codes.unauthorized:
                t = u"Les informations de connexion sont incorrectes."
                st = u"color: red;"
                self.authentication_widget.status_label.setStyleSheet(st)
                self.authentication_widget.status_label.setText(t)
                self.session = None
            else:
                self.session = None
                r.raise_for_status()
        except (ConnectionError, Exception):
            self.session = None
            log(u"Connection failed!")
            self.retry_button.setEnabled(True)
            self.taxon_dock.setWidget(self.connection_failed_widget)

    def get_whoami(self):
        try:
            headers = {
                u"Authorization": u"{} {}".format(
                    self.session[u"token_type"],
                    self.session[u"access_token"],
                )
            }
            r = requests.get(
                u"{}whoami/".format(settings.NIAMOTO_REST_BASE_URL),
                headers=headers
            )
            r.raise_for_status()
            if r.status_code == requests.codes.ok:
                whoami = json.loads(r.text)
                self.session[u"userid"] = whoami[u"id"]
                self.session[u"useremail"] = whoami[u"email"]
                self.session[u"full_name"] = whoami[u"full_name"]
                self.session[u"username"] = whoami[u"username"]
            elif r.status_code == requests.codes.unauthorized:
                self.authentication_widget.status_label.setText(
                    u"""
                    Les informations de connexon sont incorrectes.
                    """
                )
        except (ConnectionError, Exception):
            log(u"Connection failed!")
            self.retry_button.setEnabled(True)
            self.taxon_dock.setWidget(self.connection_failed_widget)

    def logout(self):
        self.session = None
        self.authenticate()

    def init_taxon_widget(self):
        try:
            self.retry_button.setEnabled(False)
            self.taxon_tree_widget = TaxonTreeWidget(self.iface, self.session)
            self.taxon_tree_widget.logout_button.clicked.connect(self.logout)
            self.taxon_dock.setWidget(self.taxon_tree_widget)
        except (ConnectionError, Exception):
            log(u"Connection failed!")
            self.retry_button.setEnabled(True)
            self.taxon_dock.setWidget(self.connection_failed_widget)

    def init_connection_failed_widget(self):
        label = QLabel(self.CONNECTION_FAILED_TEXT)
        self.retry_button = QPushButton(self.RETRY_CONNECTION_TEXT)
        self.retry_button.clicked.connect(self.authenticate)
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

    def init_authentication_widget(self):
        self.authentication_widget = AuthenticationWidget()
        self.authentication_widget.connect_button.clicked.connect(self.connect)

    def initGui(self):
        self.iface.addDockWidget(Qt.RightDockWidgetArea, self.taxon_dock)

    def run(self):
        self.taxon_dock.show()

    def unload(self):
        pass


class AuthenticationWidget(QWidget, Ui_AuthenticationWidget):

    def __init__(self, parent=None):
        super(AuthenticationWidget, self).__init__(parent)
        self.setupUi(self)

    def keyPressEvent(self, event):
        if type(event) == QKeyEvent:
            if event.key() == Qt.Key_Enter:
                self.connect_button.click()


class TaxonTreeWidget(QWidget, Ui_TaxonTreeWidget):

    def __init__(self, iface, session, parent=None):
        super(TaxonTreeWidget, self).__init__(parent)
        self.setupUi(self)
        self.iface = iface
        self.session = session
        self.username_label.setText(self.session[u"full_name"])
        log("Loading taxon tree...")
        root_items = get_taxa_tree(self.session)
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
