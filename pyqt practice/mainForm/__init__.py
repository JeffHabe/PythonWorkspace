# -*- coding: utf-8 -*-
"""
Created on Thu Jan  3 15:35:20 2019

@author: Jeff PC
"""

from PyQt5 import QtWidgets, uic
import os
path = os.getcwd()
qtCreatorFile = path + os.sep + "ui" + os.sep + "Main_Window.ui"  # 設計好的ui檔案路徑
Ui_MainWindow, QtBaseClass = uic.loadUiType(qtCreatorFile)   # 讀入用Qt Designer設計的GUI layout
