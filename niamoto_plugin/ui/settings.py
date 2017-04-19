# coding: utf-8

from PyQt4.QtGui import *

from niamoto_plugin.ui.ui_settings import Ui_NiamotoOccurrencesSettings
from niamoto_plugin import settings


class NiamotoOccurrencesSettings(QDialog, Ui_NiamotoOccurrencesSettings):

    def __init__(self, parent=None):
        super(QDialog, self).__init__(parent)
        self.setupUi(self)
        self.niamoto_base_url.setText(settings.NIAMOTO_BASE_URL)
        self.geoserver_base_url.setText(settings.GEOSERVER_BASE_URL)

    def write_settings(self):
        settings.set_niamoto_base_url(self.niamoto_base_url.text())
        settings.set_geoserver_base_url(self.geoserver_base_url.text())

