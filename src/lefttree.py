 
 
from PyQt5.QtWidgets import *
from PyQt5 import QtCore,QtGui, QtWidgets
from PyQt5.QtCore import pyqtSignal 

import psycopg2

from lib.CRUD import CRUD
import lib.Databases as Databases

class LeftTree(QWidget):

    attributeChange = pyqtSignal(int,str,str)
    attributeQuery = pyqtSignal(int,str,str)


    def __init__(self):
        super().__init__() 
        self.setupUI()

    def setupUI(self):
        #self.setGeometry(0, 0,400,2000)
        #self.setContentsMargins(0, 0, 0, 0)
      
        #Tree 생성
        self.tree = QTreeWidget(self)
        self.tree.resize(500, 1000)        
        self.tree.setColumnCount(4)
        self.tree.setColumnWidth(0,250)
        self.tree.setHeaderLabels(["구분","속성","id" ,"구분"])

        #Tree에 항목추가 (TreeWidgetItem 추가)
        itemTable = QTreeWidgetItem(self.tree)
        itemTable.setText(0,"테이블")
        itemTable.setText(1,"") 
        itemTable.setText(2,"") 
        itemTable.setText(3,"") 
        itemTable.setText(4,"") 
        
        itemQuery = QTreeWidgetItem(self.tree)
        itemQuery.setText(0,"쿼리")
        itemQuery.setText(1,"") 
        itemQuery.setText(2,"") 
        itemQuery.setText(3,"") 
        itemQuery.setText(4,"") 
 
 
           
        db = CRUD() 
        self.result = db.readDB( table="tdx_table", colum="*")
        
        for data in self.result:
            ChildA=QTreeWidgetItem(itemTable)
            
            ChildA.setText(0,data[1])
            ChildA.setText(1,data[2]) 
            ChildA.setText(2,str(data[0])) 
            ChildA.setText(3,"table") 
        
        self.result = db.readDB( table="tdx_query", colum="*")
        
        for data in self.result:
            ChildA=QTreeWidgetItem(itemQuery)
            
            ChildA.setText(0,data[2])
            ChildA.setText(1,data[1]) 
            ChildA.setText(2,str(data[0])) 
            ChildA.setText(3,"query")
        
        
        self.tree.itemClicked.connect(self.onItemClicked)
         

     
        

    @QtCore.pyqtSlot(QtWidgets.QTreeWidgetItem, int)
    def onItemClicked(self, it, col):
        print(it, col, it.text(col))
        print("mousePressEvent left Page")
        print(it.text(3))
        if(it.text(3)=='table'):
            self.attributeChange.emit(int(it.text(2)), it.text(0),it.text(1))
        if(it.text(3)=='query'):
            self.attributeQuery.emit(int(it.text(2)), it.text(0),it.text(1))

            
    


        
        

 