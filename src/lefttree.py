 
 
from PyQt5.QtWidgets import *
from PyQt5 import QtCore,QtGui, QtWidgets
from PyQt5.QtCore import pyqtSignal 

import psycopg2

from lib.CRUD import CRUD
import lib.Databases as Databases

class LeftTree(QWidget):

    attributeChange = pyqtSignal(int,str,str)

    def __init__(self):
        super().__init__() 
        self.setupUI()

    def setupUI(self):
        #self.setGeometry(0, 0,400,2000)
        #self.setContentsMargins(0, 0, 0, 0)
      
        #Tree 생성
        self.tree = QTreeWidget(self)
        self.tree.resize(500, 1000)        
        self.tree.setColumnCount(3)
        self.tree.setColumnWidth(0,250)
        self.tree.setHeaderLabels(["구분","속성","id" ])

        #Tree에 항목추가 (TreeWidgetItem 추가)
        itemA = QTreeWidgetItem(self.tree)
        itemA.setText(0,"테이블")
        itemA.setText(1,"") 
        itemA.setText(2,"") 
 
 
           
        db = CRUD() 
        self.result = db.readDB( table="tdx_table", colum="*")
        i =0
        for data in self.result:
            ChildA=QTreeWidgetItem(itemA)
            ChildA.setText(0,data[1])
            ChildA.setText(1,data[2]) 
            ChildA.setText(2,str(data[0])) 
        
        self.tree.itemClicked.connect(self.onItemClicked)
         

     
        

    @QtCore.pyqtSlot(QtWidgets.QTreeWidgetItem, int)
    def onItemClicked(self, it, col):
        print(it, col, it.text(col))
        print("mousePressEvent left Page")
        if(it.text(0)!='테이블'):
            self.attributeChange.emit(int(it.text(2)), it.text(0),it.text(1))



        
        

 