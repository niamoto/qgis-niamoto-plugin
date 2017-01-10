# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'niamoto_plugin/ui/authentication_widget.ui'
#
# Created: Fri Sep  2 14:32:26 2016
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

class Ui_AuthenticationWidget(object):
    def setupUi(self, AuthenticationWidget):
        AuthenticationWidget.setObjectName(_fromUtf8("AuthenticationWidget"))
        AuthenticationWidget.resize(323, 170)
        self.verticalLayout = QtGui.QVBoxLayout(AuthenticationWidget)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.formLayout = QtGui.QFormLayout()
        self.formLayout.setObjectName(_fromUtf8("formLayout"))
        self.label = QtGui.QLabel(AuthenticationWidget)
        self.label.setObjectName(_fromUtf8("label"))
        self.formLayout.setWidget(0, QtGui.QFormLayout.LabelRole, self.label)
        self.login_edit = QtGui.QLineEdit(AuthenticationWidget)
        self.login_edit.setObjectName(_fromUtf8("login_edit"))
        self.formLayout.setWidget(0, QtGui.QFormLayout.FieldRole, self.login_edit)
        self.label_2 = QtGui.QLabel(AuthenticationWidget)
        self.label_2.setObjectName(_fromUtf8("label_2"))
        self.formLayout.setWidget(1, QtGui.QFormLayout.LabelRole, self.label_2)
        self.password_edit = QtGui.QLineEdit(AuthenticationWidget)
        self.password_edit.setEchoMode(QtGui.QLineEdit.Password)
        self.password_edit.setObjectName(_fromUtf8("password_edit"))
        self.formLayout.setWidget(1, QtGui.QFormLayout.FieldRole, self.password_edit)
        self.verticalLayout.addLayout(self.formLayout)
        self.status_label = QtGui.QLabel(AuthenticationWidget)
        palette = QtGui.QPalette()
        brush = QtGui.QBrush(QtGui.QColor(170, 0, 0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.WindowText, brush)
        brush = QtGui.QBrush(QtGui.QColor(173, 0, 0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Text, brush)
        brush = QtGui.QBrush(QtGui.QColor(170, 0, 0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.WindowText, brush)
        brush = QtGui.QBrush(QtGui.QColor(173, 0, 0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Text, brush)
        brush = QtGui.QBrush(QtGui.QColor(143, 146, 147))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.WindowText, brush)
        brush = QtGui.QBrush(QtGui.QColor(143, 146, 147))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Text, brush)
        self.status_label.setPalette(palette)
        self.status_label.setText(_fromUtf8(""))
        self.status_label.setObjectName(_fromUtf8("status_label"))
        self.verticalLayout.addWidget(self.status_label)
        self.connect_button = QtGui.QPushButton(AuthenticationWidget)
        self.connect_button.setObjectName(_fromUtf8("connect_button"))
        self.verticalLayout.addWidget(self.connect_button)

        self.retranslateUi(AuthenticationWidget)
        QtCore.QMetaObject.connectSlotsByName(AuthenticationWidget)

    def retranslateUi(self, AuthenticationWidget):
        AuthenticationWidget.setWindowTitle(_translate("AuthenticationWidget", "Form", None))
        self.label.setText(_translate("AuthenticationWidget", "login:", None))
        self.label_2.setText(_translate("AuthenticationWidget", "mot de passe:", None))
        self.connect_button.setText(_translate("AuthenticationWidget", "Connexion", None))

