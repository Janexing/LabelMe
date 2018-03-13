#-------------------------------------------------------------------------------
# Name:        babelme.py
# Purpose:     save as gray images
#
# Author:      Administrator
#
# Created:     27/07/2017
# Copyright:   (c) Administrator 2017
# Licence:     <your licence>
#-------------------------------------------------------------------------------
# -*- coding: utf-8 -*-

import sys
sys.path.append('libs')
from ui_labelme import Ui_MainWindow
from dialog_config import Dialog_Config, CONFIG_PATH
from PyQt4 import QtGui, QtCore, QtSql
import os, time, re
from pascal_voc_io import PascalVocWriter
from ustr import ustr
from canvas import Canvas
import cv2
import ConfigParser

try:
    _encoding = QtGui.QApplication.UnicodeUTF8
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig)

class My_Window(QtGui.QMainWindow, Ui_MainWindow):

    def __init__(self, parent=None):
        super(My_Window, self).__init__(parent)
        self.setupUi(self)
        self.image_path = ""
        self.png = None

        self.canvas = Canvas()

        self.canvas.choose_category.connect(self.get_current_category)

        self.dialog_config = Dialog_Config()
        self.dialog_config.dialog_addlabel.config_refresh.connect(self.show_color_list)
        self.dialog_config.delete_refresh.connect(self.show_color_list)
        self.show_color_list()

        QtCore.QObject.connect(self.pushButton_Open, QtCore.SIGNAL('clicked()'), self.open)
        QtCore.QObject.connect(self.pushButton_Create, QtCore.SIGNAL('clicked()'), self.create)
        QtCore.QObject.connect(self.pushButton_Save, QtCore.SIGNAL('clicked()'), self.save)
        QtCore.QObject.connect(self.pushButton_NextImage, QtCore.SIGNAL('clicked()'), self.open_nextimg)
        QtCore.QObject.connect(self.pushButton_PrevImage, QtCore.SIGNAL('clicked()'), self.open_previmg)
        QtCore.QObject.connect(self.pushButton_Delete, QtCore.SIGNAL('clicked()'), self.canvas.delete_line)
        QtCore.QObject.connect(self.toolButton_Config, QtCore.SIGNAL('clicked()'), self.dialog_config.show)


        QtCore.QObject.connect(self.actionOpen, QtCore.SIGNAL('activated()'), self.open)
        QtCore.QObject.connect(self.actionSave, QtCore.SIGNAL('activated()'), self.save)
        QtCore.QObject.connect(self.actionClose, QtCore.SIGNAL('activated()'), self.close)
        QtCore.QObject.connect(self.actionCreate_Pixmap, QtCore.SIGNAL('activated()'), self.create)
        QtCore.QObject.connect(self.actionDelete, QtCore.SIGNAL('activated()'), self.canvas.delete_line)

    def show_color_list(self):
        for item in self.label_Category_list:
            item.setVisible(False)
        for item in self.label_color_list:
            item.setVisible(False)
        cf = ConfigParser.ConfigParser()
        cf.read(CONFIG_PATH)
        section_list = cf.sections()
        pattern = re.compile(r'^label_')
        section_color = [item for item in section_list if pattern.match(item)!=None]
        for item in section_color:
            section_num = int(item.split('_')[-1])
            bgr_value = cf.get(item, 'bgr value')
            gray_value = cf.get(item, 'gray value')
            #print bgr_value
            tmp = bgr_value[1:-1].split(',')
            r = int(tmp[2])
            g = int(tmp[1])
            b = int(tmp[0])
            label_name = cf.get(item, 'label name')
            self.canvas.bgr_list[unicode(label_name)] = bgr_value
            self.canvas.gray_list[unicode(label_name)] = gray_value
            self.label_Category_list[section_num-1].setVisible(True)
            self.label_Category_list[section_num-1].setText(_translate("MainWindow", unicode(label_name), None))
            self.label_color_list[section_num-1].setVisible(True)
            self.label_color_list[section_num-1].setStyleSheet("background-color:rgb(%d, %d, %d)" % (r, g, b))
            if section_color.index(item) == 0:
                self.label_Category_list[section_num-1].setChecked(True)

    def get_current_category(self):
        for item in self.label_Category_list:
            if item.isVisible() and item.isChecked():
                self.canvas.object = item.text()

    def open_nextimg(self):
        image_list = []
        #print self.image_path
        dir_path1 = ustr(self.image_path).split('/')[:-1]
        current_image = ustr(self.image_path).split('/')[-1]
        dir_path = '/'.join(dir_path1)
        #print dir_path
        dir_items = os.listdir(dir_path)
        for item in dir_items:
            if item.endswith('.jpg') or item.endswith('.png') or item.endswith('.jpeg'):
                image_list.append(item)
        if image_list.index(current_image) == len(image_list)-1:
             QtGui.QMessageBox.information(self,"Information", u"已经最后一张了！")
             return
        current_image_index = image_list.index(current_image) + 1
        next_image = dir_path + '/' + image_list[current_image_index]
        #print next_image
        png = QtGui.QPixmap(next_image).scaled(self.label_Image.width(), self.label_Image.height())
        self.label_Image.setPixmap(png)
        self.image_path = next_image
        #self.label_imagepath.setText(self.image_path)
        self.setWindowTitle(_translate("MainWindow", "LabelMe"+" "+ustr(self.image_path), None))

    def open_previmg(self):
        image_list = []
        dir_path1 = ustr(self.image_path).split('/')[:-1]
        current_image = ustr(self.image_path).split('/')[-1]
        dir_path = '/'.join(dir_path1)
        dir_items = os.listdir(dir_path)
        for item in dir_items:
            if item.endswith('.jpg') or item.endswith('.png') or item.endswith('.jpeg'):
                image_list.append(item)
        #print image_list
        #print image_list.index(current_image)
        if image_list.index(current_image) == 0:
             QtGui.QMessageBox.information(self,"Information", u"已经是第一张了！")
             return
        current_image_index = image_list.index(current_image) - 1
        next_image = dir_path + '/' + image_list[current_image_index]
        png = QtGui.QPixmap(next_image).scaled(self.label_Image.width(), self.label_Image.height())
        self.label_Image.setPixmap(png)
        self.image_path = next_image
        #self.label_imagepath.setText(self.image_path)
        self.setWindowTitle(_translate("MainWindow", "LableMe"+" "+ustr(self.image_path), None))

    def open(self):
        img_name= ustr(QtGui.QFileDialog.getOpenFileName(self,'Open file',".","*.jpg;;*.png;;*.jpeg;;*.bmp;;All Files (*)"))
        #print unicode(img_name, 'ascii')
        print(img_name)
        self.png = QtGui.QPixmap(img_name).scaled(self.label_Image.width(), self.label_Image.height())
        self.label_Image.setPixmap(self.png)
        self.image_path = img_name
        #self.image_path.setText(self.image_path)
        self.setWindowTitle(_translate("MainWindow", "LabelMe"+" "+ustr(self.image_path), None))


    def open_dir(self):
        tmp_dir = QtGui.QFileDialog.getExistingDirectory()
        #self.lineEdit_6.setText(tmp_dir)


    def save(self):
        if self.image_path == "":
             QtGui.QMessageBox.information(self,"Information", u"请先打开一张图片！")
             return
        self.canvas.destroy_img_windows()
        self.write_xml()
        self.canvas.index_num = 0
        #self.label_dialog.show()

    def save_file(self):
        if self.image_path:
            image_file_name = ustr(self.image_path).split('.')[0]
            saved_file_name = image_file_name + '.xml'

    def write_xml(self):
        imgFolderName = ustr(self.image_path).split('/')[-2]
        print imgFolderName
        #imgFileName = str(self.image_path).split('/')[-1]
        imgFileNameWithoutExt = ustr(self.image_path).split('.')[0]
        print imgFileNameWithoutExt

        image = QtGui.QImage()
        image.load(ustr(self.image_path))
        imageShape = [image.height(), image.width(),
                      1 if image.isGrayscale() else 3]
        writer = PascalVocWriter(imgFolderName, imgFileNameWithoutExt,
                                 imageShape, localImgPath=ustr(self.image_path))
        #writer.verified = self.verified
        item = {}
        item['name'] = ''
        item['flood1name'] = imgFileNameWithoutExt + '_index.bmp'
        item['flood2name'] = imgFileNameWithoutExt + '_category.bmp'
        writer.addObject(item['name'], item['flood1name'], item['flood2name'])

        writer.save()
        return

    def draw(self,event,x,y,flags,param):
        print '1111'
        if event == cv2.EVENT_LBUTTONDOWN:
            print '2222'
            #self.points.append((x,y))
            cv2.circle(self.label_Image.pixmap,(x,y),2,(0,0,255),2)
            #cv2.circle(self.image,(x,y),2,(0,0,255),2)
            #cv2.circle(self.mask,(x,y),2,(255,255,255),2)
            print self.points
            cv2.imshow('MainWindow', self.image)

    def create(self):
        self.canvas.image_path = self.image_path
        self.canvas.create()

if __name__ == '__main__':
    app = QtGui.QApplication(sys.argv)
    myshow = My_Window()
    myshow.show()
    sys.exit(app.exec_())
