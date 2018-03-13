#-------------------------------------------------------------------------------
# Name:
# Purpose:
#
# Author:      Administrator
#
# Created:     21/11/2017
# Copyright:   (c) Administrator 2017
# Licence:     <your licence>
#-------------------------------------------------------------------------------
# -*- coding = utf-8 -*-

import os
from ustr import ustr
import cv2
import numpy as np
import copy
import random

try:
    from PyQt5.QtGui import *
    from PyQt5.QtCore import *
    from PyQt5.QtWidgets import *
except ImportError:
    from PyQt4.QtGui import *
    from PyQt4.QtCore import *

class Canvas(QWidget):
    bgr_list = {}
    gray_list = {}

    EDIT, CREATE = list(range(2))
    choose_category = pyqtSignal()

    def __init__(self, parent=None, image_path=None):
        super(Canvas, self).__init__(parent)
        self.image_path = image_path
        self.mode = self.EDIT
        self.image = None
        self.flooded = None
        self.drawing = False
        self.mask_ = None
        self.object = u'人'
        self.ix = -1
        self.iy = -1
        self.flooded2 = None
        self.flooded2_tmp = None
        self.points = []
        self.pre_pos = None
        #self.first_pos = None
        self.index_num = 0
        self.png = None

    def isEqual(self, point1, point2):
        xsub = int(point1[0]) - int(point2[0])
        ysub = int(point1[1]) - int(point2[1])
        if abs(xsub) < 5 and abs(ysub) < 5:
            return True
        else:
            return False

    def delete_line(self):
        if self.pre_pos is not None:
            point1 = self.points.pop()
            #print point1
            point2 = self.points.pop()
            #print point2
            cv2.circle(self.image,point1,2,(0,0,0),2)
            cv2.circle(self.mask,point1,2,(0,0,0),2)
            cv2.circle(self.image,point2,2,(0,0,0),2)
            cv2.circle(self.mask,point2,2,(0,0,0),2)
            cv2.line(ustr(self.image), point2, point1, (0,0,0),2)
            cv2.line(self.mask, point2, point1, (0,0,0), 2)
            cv2.imshow('image', self.image)
            self.pre_pos = None

    def draw(self,event,x,y,flags,param):
        #self.save_file()
        fixed_range=True
        path = ustr(self.image_path).split('.')[0]
        suffix = 'bmp'
        #print path
        mask_name = path + '_mask.' + suffix
        flood_name = path + '_index.' + suffix
        flood2_name = path + '_category.' + suffix

        self.choose_category.emit()

        if event == cv2.EVENT_LBUTTONDOWN:
            self.points.append((x,y))
            #cv2.circle(self.label_Image.pixmap,(x,y),2,(0,0,255),2)
            cv2.circle(self.image,(x,y),2,(0,0,255),2)
            cv2.circle(self.mask,(x,y),2,(255,255,255),2)
            #print self.points
            #print self.pre_pos

            if self.pre_pos is not None:
                cv2.line(ustr(self.image), self.pre_pos, (x,y), (0,255,0),2)
                cv2.line(self.mask, self.pre_pos, (x,y), (255,255,255), 2)
                if self.isEqual(self.points[0],self.points[-1]):
                    cv2.line(ustr(self.image), (x,y), self.points[0], (0,255,0),2)
                    cv2.line(self.mask, (x,y), self.points[0], (255,255,255), 2)
                    self.pre_pos = None
                    self.points = []
                else:
                    self.pre_pos = (x, y)
            else:
                #self.first_pos = (x, y)
                self.pre_pos = (x, y)
            self.mask_ = self.mask.copy()
            self.mask2_ = self.mask.copy()
            cv2.imshow('image', self.image)
            #cv2.imshow('mask', self.mask)
            #self.pre_pos = (x, y)

        #elif event == cv2.EVENT_LBUTTONDBLCLK:
        #    QtGui.QMessageBox.information(self,"Information", u"确定删除？")

        elif event == cv2.EVENT_RBUTTONUP:
            self.pre_pos = None
    	    #print(self.mask.dtype)
    	    fixed_range=True
    	    flags=8
            #print 'step 1'

            #点击到区域外撤销
            tmp_mask2_ = self.mask.copy()
            tmp = self.bgr_list[ustr(self.object)]
            if self.flooded.item(y,x) != 0 or self.flooded2.item(y,x) != 0 :
                cv2.floodFill(self.flooded2_show, tmp_mask2_, (x,y), (0,0,0), (0,)*3, (0,)*3, flags)
                cv2.floodFill(self.flooded, self.mask_, (x,y), 0, (255,)*3, (160,)*3, flags)
                cv2.floodFill(self.flooded2, self.mask2_, (x,y), 0, (255,)*3, (160,)*3, flags)
                #cv2.imshow('index',self.flooded)
                cv2.imshow('category',self.flooded2_show)
                cv2.imencode('.bmp',self.flooded)[1].tofile(ustr(flood_name))
                cv2.imencode('.bmp',self.flooded2)[1].tofile(ustr(flood2_name))
                #self.index_num = self.index_num - 1
            else:
                self.index_num = self.index_num + 1
                tmp_mask = self.mask.copy()
                print self.index_num
                #cv2.floodFill(self.flooded, tmp_mask, (x,y), (random.randint(0,255), random.randint(0,255), random.randint(0,255)), (0,)*3, (0,)*3, 4)
                cv2.floodFill(self.flooded, tmp_mask, (x,y), self.index_num, (0,)*3, (0,)*3, 4)
                mask_gray=self.mask.copy()
                res,thres=cv2.threshold(mask_gray,0,255,cv2.THRESH_BINARY)
                thresgray=cv2.cvtColor(thres,cv2.COLOR_GRAY2BGR)
                #cv2.imshow('index',self.flooded)
                cv2.imencode('.bmp',self.flooded)[1].tofile(ustr(flood_name))

                tmp_mask2 = self.mask.copy()
                tmp_mask3 = self.mask.copy()

                print self.bgr_list[unicode(self.object)]
                tmp = self.bgr_list[unicode(self.object)][1:-1].split(',')
                b = int(tmp[0])
                g = int(tmp[1])
                r = int(tmp[2])
                print self.gray_list[unicode(self.object)]

                cv2.floodFill(self.flooded2_show, tmp_mask3, (x,y), (b, g, r),  (0,)*3, (0,)*3, flags)
                cv2.floodFill(self.flooded2, tmp_mask2, (x,y), int(self.gray_list[unicode(self.object)]),  (0,)*3, (0,)*3, flags)
                cv2.imshow('category',self.flooded2_show)
                cv2.imencode('.bmp',self.flooded2)[1].tofile(ustr(flood2_name))


    def create(self):
        self.mode = self.CREATE
        if self.image_path == "":
             QMessageBox.information(self,"Information", u"请先打开一张图片！")
             return
        if os.path.exists(ustr(self.image_path)+'.xml'):
            os.rm(ustr(self.image_path)+'.xml')
        self.points = []
        self.pre_pos = None
        #1:bgr  0:grayscale
        self.image = cv2.imdecode(np.fromfile(ustr(self.image_path), dtype=np.uint8), 1)
        #self.image = cv2.imdecode(self.label_Image.pixmap, 1)
        self.image_gray = cv2.imdecode(np.fromfile(ustr(self.image_path), dtype=np.uint8), 0)
        h, w = self.image.shape[:2]
        self.mask = np.zeros((h+2, w+2), np.uint8)
        self.flooded = copy.deepcopy(self.image_gray)
        self.flooded[:]=0
        self.flooded2 = copy.deepcopy(self.image_gray)
        self.flooded2[:]=0
        self.flooded2_show = copy.deepcopy(self.image)
        self.flooded2_show[:]=0
        self.mask[:] = 0
        cv2.namedWindow('image', cv2.WINDOW_KEEPRATIO | cv2.WINDOW_NORMAL)
        cv2.imshow('image',self.image)
        cv2.setMouseCallback('image',self.draw)

    def out_of_pixmap(self, p):
        w, h = self.image.width(), self.image.height()
        return not (0 <= p.x() <= w and 0 <= p.y() <= h)

    def destroy_img_windows(self):
        cv2.destroyAllWindows()

if __name__ == '__main__':
    main()
