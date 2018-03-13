# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'dialog_add_label.ui'
#
# Created by: PyQt4 UI code generator 4.11.4
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

class Ui_Dialog_addLabel(object):
    def setupUi(self, Dialog_addLabel):
        Dialog_addLabel.setObjectName(_fromUtf8("Dialog_addLabel"))
        Dialog_addLabel.resize(400, 272)
        self.buttonBox_cancel = QtGui.QDialogButtonBox(Dialog_addLabel)
        self.buttonBox_cancel.setGeometry(QtCore.QRect(300, 50, 81, 241))
        self.buttonBox_cancel.setOrientation(QtCore.Qt.Vertical)
        self.buttonBox_cancel.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Ok)
        self.buttonBox_cancel.setObjectName(_fromUtf8("buttonBox_cancel"))
        self.lineEdit_name = QtGui.QLineEdit(Dialog_addLabel)
        self.lineEdit_name.setGeometry(QtCore.QRect(100, 20, 150, 20))
        self.lineEdit_name.setObjectName(_fromUtf8("lineEdit_name"))
        self.lineEdit_grayValue = QtGui.QLineEdit(Dialog_addLabel)
        self.lineEdit_grayValue.setGeometry(QtCore.QRect(100, 50, 150, 20))
        self.lineEdit_grayValue.setObjectName(_fromUtf8("lineEdit_grayValue"))
        self.textEdit_labelDescription = QtGui.QTextEdit(Dialog_addLabel)
        self.textEdit_labelDescription.setGeometry(QtCore.QRect(20, 110, 231, 121))
        self.textEdit_labelDescription.setObjectName(_fromUtf8("textEdit_labelDescription"))
        self.label_labelDescription = QtGui.QLabel(Dialog_addLabel)
        self.label_labelDescription.setGeometry(QtCore.QRect(20, 80, 321, 16))
        self.label_labelDescription.setObjectName(_fromUtf8("label_labelDescription"))
        self.label_name = QtGui.QLabel(Dialog_addLabel)
        self.label_name.setGeometry(QtCore.QRect(20, 20, 71, 16))
        self.label_name.setObjectName(_fromUtf8("label_name"))
        self.label_grayValue = QtGui.QLabel(Dialog_addLabel)
        self.label_grayValue.setGeometry(QtCore.QRect(20, 50, 71, 16))
        self.label_grayValue.setObjectName(_fromUtf8("label_name"))

        self.retranslateUi(Dialog_addLabel)
        #QtCore.QObject.connect(self.buttonBox_cancel, QtCore.SIGNAL(_fromUtf8("accepted()")), Dialog_addLabel.accept)
        #QtCore.QObject.connect(self.buttonBox_cancel, QtCore.SIGNAL(_fromUtf8("rejected()")), Dialog_addLabel.reject)
        #QtCore.QMetaObject.connectSlotsByName(Dialog_addLabel)

    def retranslateUi(self, Dialog_addLabel):
        Dialog_addLabel.setWindowTitle(_translate("Dialog_addLabel", "增加", None))
        self.label_labelDescription.setText(_translate("Dialog_addLabel", "Label Description(Optional)", None))
        self.label_name.setText(_translate("Dialog_addLabel", "Label Name", None))
        self.label_grayValue.setText(_translate("Dialog_addLabel", "Gray Value", None))

