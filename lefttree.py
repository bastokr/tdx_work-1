 
 
from PyQt5.QtWidgets import *
from PyQt5 import QtCore,QtGui, QtWidgets
from PyQt5.QtCore import pyqtSignal 

import psycopg2

from CRUD import CRUD
import Databases

class LeftTree(QWidget):

    closeApp = pyqtSignal()

    def __init__(self):
        super().__init__() 
        self.setupUI()

    def setupUI(self):
        #self.setGeometry(0, 0,400,2000)
        #self.setContentsMargins(0, 0, 0, 0)
      
        #Tree 생성
        self.tree = QTreeWidget(self)
        self.tree.resize(300, 1000)        
        self.tree.setColumnCount(2)
        self.tree.setColumnWidth(0,150)
        self.tree.setHeaderLabels(["구분","속성" ])

        #Tree에 항목추가 (TreeWidgetItem 추가)
        itemA = QTreeWidgetItem(self.tree)
        itemA.setText(0,"테이블")
        itemA.setText(1,"테이블") 
 
 
           
        db = CRUD() 
        result = db.readDB( table="menu_mgmt", colum="*")
        i =0
        for data in result:
            ChildA=QTreeWidgetItem(itemA)
            ChildA.setText(0,data[1])
            ChildA.setText(1,data[0]) 
        
        self.tree.itemClicked.connect(self.onItemClicked)
         

     
        

    @QtCore.pyqtSlot(QtWidgets.QTreeWidgetItem, int)
    def onItemClicked(self, it, col):
        print(it, col, it.text(col))
        print("mousePressEvent left Page")
        self.closeApp.emit()



        
        

 