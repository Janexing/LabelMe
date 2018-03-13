# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'gui/Dialogsui.ui'
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

class Ui_DialogConfig(object):
    def setupUi(self, DialogConfig):
        DialogConfig.setObjectName(_fromUtf8("DialogConfig"))
        DialogConfig.resize(396, 300)
        self.pushButton_Add = QtGui.QPushButton(DialogConfig)
        #self.pushButton_Add.setGeometry(QtCore.QRect(30, 260, 75, 23))
        self.pushButton_Add.setGeometry(QtCore.QRect(30, 20, 75, 23))
        self.pushButton_Add.setObjectName(_fromUtf8("pushButton_Connect"))
        self.pushButton_Cancel = QtGui.QPushButton(DialogConfig)
        self.pushButton_Cancel.setGeometry(QtCore.QRect(240, 260, 75, 23))
        self.pushButton_Cancel.setObjectName(_fromUtf8("pushButton_Cancel"))
        self.pushButton_Clear = QtGui.QPushButton(DialogConfig)
        self.pushButton_Clear.setGeometry(QtCore.QRect(120, 260, 75, 23))
        self.pushButton_Clear.setObjectName(_fromUtf8("pushButton_Clear"))
        #self.pushButton_Change.setEnabled(False)
        self.listTable_DialogList = QtGui.QTableWidget(DialogConfig)
        self.listTable_DialogList.setGeometry(QtCore.QRect(20, 50, 361, 192))
        self.listTable_DialogList.setObjectName(_fromUtf8("listTable_DialogList"))
        self.listTable_DialogList.setColumnCount(3)
        self.listTable_DialogList.setRowCount(20)
        item = QtGui.QTableWidgetItem()
        self.listTable_DialogList.setVerticalHeaderItem(0, item)
        item = QtGui.QTableWidgetItem()
        self.listTable_DialogList.setHorizontalHeaderItem(0, item)
        item = QtGui.QTableWidgetItem()
        self.listTable_DialogList.setHorizontalHeaderItem(1, item)
        item = QtGui.QTableWidgetItem()
        self.listTable_DialogList.setHorizontalHeaderItem(2, item)
        #self.listTable_DialogList.resizeColumnsToContents()
        self.listTable_DialogList.horizontalHeader().setDefaultSectionSize(100)
        self.listTable_DialogList.verticalHeader().setDefaultSectionSize(20)
        self.retranslateUi(DialogConfig)
        QtCore.QMetaObject.connectSlotsByName(DialogConfig)

    def retranslateUi(self, DialogConfig):
        DialogConfig.setWindowTitle(_translate("DialogConfig", "目标配置", None))
        self.pushButton_Add.setText(_translate("DialogConfig", "增加", None))
        self.pushButton_Cancel.setText(_translate("DialogConfig", "关闭", None))
        self.pushButton_Clear.setText(_translate("DialogConfig", "删除", None))
        item = self.listTable_DialogList.verticalHeaderItem(0)
        item.setText(_translate("DialogConfig", "1", None))
        item = self.listTable_DialogList.horizontalHeaderItem(0)
        item.setText(_translate("DialogConfig", "Name", None))
        item = self.listTable_DialogList.horizontalHeaderItem(1)
        item.setText(_translate("DialogConfig", "BGR value", None))
        item = self.listTable_DialogList.horizontalHeaderItem(2)
        item.setText(_translate("DialogConfig", "color", None))


