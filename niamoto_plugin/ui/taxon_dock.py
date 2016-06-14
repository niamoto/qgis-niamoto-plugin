# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'niamoto_plugin/ui/taxon_dock.ui'
#
# Created: Tue Jun 14 10:48:39 2016
#      by: PyQt4 UI code generator 4.11.2
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s

try:
    _encoding = QtGui.QApplication.UnicodeUTF8
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig)

class Ui_TaxonTreeWidget(object):
    def setupUi(self, TaxonTreeWidget):
        TaxonTreeWidget.setObjectName(_fromUtf8("TaxonTreeWidget"))
        TaxonTreeWidget.resize(661, 624)
        self.verticalLayout_2 = QtGui.QVBoxLayout(TaxonTreeWidget)
        self.verticalLayout_2.setObjectName(_fromUtf8("verticalLayout_2"))
        self.tabWidget = QtGui.QTabWidget(TaxonTreeWidget)
        self.tabWidget.setObjectName(_fromUtf8("tabWidget"))
        self.occurrences_tab = QtGui.QWidget()
        self.occurrences_tab.setObjectName(_fromUtf8("occurrences_tab"))
        self.verticalLayout = QtGui.QVBoxLayout(self.occurrences_tab)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.filter_edit = QtGui.QLineEdit(self.occurrences_tab)
        self.filter_edit.setAutoFillBackground(False)
        self.filter_edit.setStyleSheet(_fromUtf8("background-color: rgb(255, 255, 255);"))
        self.filter_edit.setObjectName(_fromUtf8("filter_edit"))
        self.horizontalLayout.addWidget(self.filter_edit)
        self.filter_button = QtGui.QPushButton(self.occurrences_tab)
        self.filter_button.setObjectName(_fromUtf8("filter_button"))
        self.horizontalLayout.addWidget(self.filter_button)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.horizontalLayout_2 = QtGui.QHBoxLayout()
        self.horizontalLayout_2.setObjectName(_fromUtf8("horizontalLayout_2"))
        self.expand_button = QtGui.QPushButton(self.occurrences_tab)
        self.expand_button.setObjectName(_fromUtf8("expand_button"))
        self.horizontalLayout_2.addWidget(self.expand_button)
        self.collapse_button = QtGui.QPushButton(self.occurrences_tab)
        self.collapse_button.setObjectName(_fromUtf8("collapse_button"))
        self.horizontalLayout_2.addWidget(self.collapse_button)
        spacerItem = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem)
        self.verticalLayout.addLayout(self.horizontalLayout_2)
        self.taxon_treeview = QtGui.QTreeView(self.occurrences_tab)
        self.taxon_treeview.setAlternatingRowColors(True)
        self.taxon_treeview.setObjectName(_fromUtf8("taxon_treeview"))
        self.verticalLayout.addWidget(self.taxon_treeview)
        self.frame = QtGui.QFrame(self.occurrences_tab)
        self.frame.setFrameShape(QtGui.QFrame.Panel)
        self.frame.setFrameShadow(QtGui.QFrame.Raised)
        self.frame.setObjectName(_fromUtf8("frame"))
        self.gridLayout = QtGui.QGridLayout(self.frame)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.label_3 = QtGui.QLabel(self.frame)
        self.label_3.setObjectName(_fromUtf8("label_3"))
        self.gridLayout.addWidget(self.label_3, 0, 0, 1, 1)
        self.taxon_label = QtGui.QLabel(self.frame)
        font = QtGui.QFont()
        font.setFamily(_fromUtf8("Cantarell"))
        font.setPointSize(11)
        font.setBold(True)
        font.setItalic(False)
        font.setWeight(75)
        font.setKerning(True)
        self.taxon_label.setFont(font)
        self.taxon_label.setStyleSheet(_fromUtf8("font: 600 11pt \"Cantarell\";"))
        self.taxon_label.setText(_fromUtf8(""))
        self.taxon_label.setAlignment(QtCore.Qt.AlignCenter)
        self.taxon_label.setObjectName(_fromUtf8("taxon_label"))
        self.gridLayout.addWidget(self.taxon_label, 0, 1, 1, 2)
        self.wfs_button = QtGui.QPushButton(self.frame)
        self.wfs_button.setObjectName(_fromUtf8("wfs_button"))
        self.gridLayout.addWidget(self.wfs_button, 3, 0, 1, 3)
        self.verticalLayout.addWidget(self.frame)
        self.all_occurrences_button = QtGui.QPushButton(self.occurrences_tab)
        self.all_occurrences_button.setObjectName(_fromUtf8("all_occurrences_button"))
        self.verticalLayout.addWidget(self.all_occurrences_button)
        self.tabWidget.addTab(self.occurrences_tab, _fromUtf8(""))
        self.massifs_tab = QtGui.QWidget()
        self.massifs_tab.setObjectName(_fromUtf8("massifs_tab"))
        self.tabWidget.addTab(self.massifs_tab, _fromUtf8(""))
        self.verticalLayout_2.addWidget(self.tabWidget)

        self.retranslateUi(TaxonTreeWidget)
        self.tabWidget.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(TaxonTreeWidget)

    def retranslateUi(self, TaxonTreeWidget):
        TaxonTreeWidget.setWindowTitle(_translate("TaxonTreeWidget", "Form", None))
        self.filter_button.setText(_translate("TaxonTreeWidget", "Filtrer", None))
        self.expand_button.setText(_translate("TaxonTreeWidget", "Développer", None))
        self.collapse_button.setText(_translate("TaxonTreeWidget", "Réduire", None))
        self.label_3.setText(_translate("TaxonTreeWidget", "Taxon:", None))
        self.wfs_button.setText(_translate("TaxonTreeWidget", "Ajouter la couche du taxon", None))
        self.all_occurrences_button.setText(_translate("TaxonTreeWidget", "Ajouter toutes les occurrences", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.occurrences_tab), _translate("TaxonTreeWidget", "Occurrences", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.massifs_tab), _translate("TaxonTreeWidget", "Massifs", None))

