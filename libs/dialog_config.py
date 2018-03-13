#-------------------------------------------------------------------------------
# Name:        dialog_config.py
# Purpose:
#
# Author:      Administrator
#
# Created:     23/11/2017
# Copyright:   (c) Administrator 2017
# Licence:     <your licence>
#-------------------------------------------------------------------------------
# -*- coding = utf-8 -*-
from PyQt4 import QtGui, QtCore, QtSql
from ui_config import Ui_DialogConfig
from ui_add_label import Ui_Dialog_addLabel
import ConfigParser
import os, random, re

CONFIG_PATH = 'config/labelme.conf'

class Dialog_Config(QtGui.QWidget, Ui_DialogConfig):
    delete_refresh = QtCore.pyqtSignal()

    def __init__(self, parent=None):
        super(Dialog_Config, self).__init__(parent)
        self.setupUi(self)
        self.init_config()
        self.show_config()
        self.dialog_addlabel = Dialog_Add_Label()
        self.dialog_addlabel.config_refresh.connect(self.show_config)

        QtCore.QObject.connect(self.pushButton_Add, QtCore.SIGNAL('clicked()'), self.dialog_addlabel.show)
        QtCore.QObject.connect(self.pushButton_Clear, QtCore.SIGNAL('clicked()'), self.delete_config)
        QtCore.QObject.connect(self.pushButton_Cancel, QtCore.SIGNAL('clicked()'), self.close)

    def init_config(self):
        if not os.path.exists(CONFIG_PATH):
            os.system(r'touch %s' % CONFIG_PATH)
            cf = ConfigParser.ConfigParser()
            cf.read(CONFIG_PATH)
            cf.add_section('all')
            cf.set('all', 'number', 0)
            cf.write(open(CONFIG_PATH, 'w'))

    def show_config(self):
        self.listTable_DialogList.clear()
        cf = ConfigParser.ConfigParser()
        cf.read(CONFIG_PATH)
        number = cf.get('all', 'number')
        print number
        section_list = cf.sections()
        pattern = re.compile(r'^label_')
        label_list = [item for item in section_list if pattern.match(item)!=None]
        print label_list

        for item in label_list:
            i = int(item.split('_')[-1])-1
            name = cf.get(item, "label name")
            widget_item = QtGui.QTableWidgetItem(unicode(name))
            self.listTable_DialogList.setItem(i,0,widget_item)
            bgr_value = cf.get(item, "bgr value")
            widget_item = QtGui.QTableWidgetItem(bgr_value)
            self.listTable_DialogList.setItem(i,1,widget_item)
            #bgr = save_config.get(item, "bgr value")
            #widget_item = QtGui.QTableWidgetItem(bgr)
            #self.listTable_DialogList.setItem(i,2,widget_item)

    def delete_config(self):
        print self.listTable_DialogList.selectedItems()
        if self.listTable_DialogList.selectedItems() == []:
            QtGui.QMessageBox.information(self,"Information", u"请选择要删除的行！")
        cf = ConfigParser.ConfigParser()
        cf.read(CONFIG_PATH)
        number = cf.get('all', 'number')
        #items = self.listTable_DialogList.selectedItems()
        row_number = self.listTable_DialogList.currentRow()+1
        section_name = 'label_'+str(row_number)
        print section_name
        if section_name in cf.sections():
            cf.remove_section(section_name)
            number = int(number) - 1
        cf.set('all', 'number', number)
        cf.write(open(CONFIG_PATH, 'w'))
        self.show_config()
        self.delete_refresh.emit()

class Dialog_Add_Label(QtGui.QWidget, Ui_Dialog_addLabel):

    config_refresh = QtCore.pyqtSignal()

    def __init__(self, parent=None):
        super(Dialog_Add_Label, self).__init__(parent)
        self.setupUi(self)
        self.number = self.get_number()

        QtCore.QObject.connect(self.buttonBox_cancel, QtCore.SIGNAL("accepted()"), self.accept)
        QtCore.QObject.connect(self.buttonBox_cancel, QtCore.SIGNAL("rejected()"), self.reject)

    def get_number(self):
        cf = ConfigParser.ConfigParser()
        cf.read(CONFIG_PATH)
        number = cf.get('all', 'number')
        return int(number)

    def accept(self):
        self.number = self.number + 1
        cf = ConfigParser.ConfigParser()
        cf.read(CONFIG_PATH)
        section_name = "label_" + str(self.number)
        cf.add_section(section_name)
        label_name = self.lineEdit_name.text()
        label_desc = self.textEdit_labelDescription.toPlainText()
        bgr_value = (random.randint(0,255), random.randint(0,255), random.randint(0,255))
        gray_value = self.lineEdit_grayValue.text()
        cf.set(section_name, "label name", label_name)
        cf.set(section_name, "label description", label_desc)
        cf.set(section_name, "bgr value", bgr_value)
        cf.set(section_name, "gray value", gray_value)
        cf.set('all', 'number', self.number)
        cf.write(open(CONFIG_PATH, 'w'))
        QtGui.QMessageBox.information(self,"Information", u"增加成功！")
        self.config_refresh.emit()

    def reject(self):
        self.lineEdit_name.clear()
        self.textEdit_labelDescription.clear()

if __name__ == '__main__':
    main()
