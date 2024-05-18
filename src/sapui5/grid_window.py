import html
import os
import sys
from turtle import width
from PyQt5.QtWidgets import QApplication,QTableWidgetItem, QTableWidget,QAbstractItemView,QMainWindow, QWidget, QVBoxLayout, QTextEdit, QPushButton
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont
import xml.etree.ElementTree as ET
import xml.dom.minidom

from lib.crud import Crud


class GridWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.tableWidget = QTableWidget();

        self.setWindowTitle("PyQt5 Code Viewer and Executor")
        self.setGeometry(100, 100, 800, 600)

        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        self.layout = QVBoxLayout()
        self.central_widget.setLayout(self.layout)
 
         

        self.execute_button = QPushButton("Execute")
        self.execute_button.clicked.connect(self.execute_code)
        self.layout.addWidget(self.execute_button, alignment=Qt.AlignRight)
        
         
        self.tableWidget.setColumnCount(10)

        self.tableWidget.setEditTriggers(QAbstractItemView.NoEditTriggers) # type: ignore
        # self.tableWidget.setEditTriggers(QAbstractItemView.DoubleClicked)
        # self.tableWidget.setEditTriggers(QAbstractItemView.AllEditTriggers)
        
        self.tableWidget.setHorizontalHeaderLabels(["선택","id", "테이브id","컬럼명","타입"])  
        #self.tableWidget.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.tableWidget.horizontalHeader().resizeSection(0,50)
        
        self.layout.addWidget(self.tableWidget)
        
    
    def default_param(self,id ):
        
        db = Crud()
        self.id = id; 
        #self.result , colnames = db.whereDB( table="tdx_query", column="*" , where ="id='"+id+"'",return_column_names=True)
        
        self.result , colnames = db.execute("select * from member", return_column_names=True)
        
        self.tableWidget.setColumnCount(len(colnames))
        self.tableWidget.setHorizontalHeaderLabels(colnames)  
        self.tableWidget.setRowCount(len(self.result))

        
        for i, data in enumerate(self.result): 
             
            for j, value in enumerate(data):
                item = QTableWidgetItem(str(value))
                item.setTextAlignment( Qt.AlignCenter)

                self.tableWidget.setItem(i, j, item)
            
            #self.tableWidget.cellChanged.connect(self.onCellChanged)
       
        
        i =0
      #result.count
        
         
                

    def showGrid(self,query_text):
        print(query_text)
        db = Crud()
        self.id = id; 
        self.result , colnames = db.execute(query_text, return_column_names=True)
        self.tableWidget.clear()
        self.tableWidget.setColumnCount(len(colnames))
        self.tableWidget.setHorizontalHeaderLabels(colnames)  
        self.tableWidget.setRowCount(len(self.result))

        
        for i, data in enumerate(self.result): 
             
            for j, value in enumerate(data):
                item = QTableWidgetItem(str(value))
                item.setTextAlignment( Qt.AlignCenter)

                self.tableWidget.setItem(i, j, item)
            
            #self.tableWidget.cellChanged.connect(self.onCellChanged)
       
        
         
         

    def execute_code(self):
        code = self.code_editor.toPlainText()
        
        try:
            exec(code)
        except Exception as e:
            print("An error occurred:", e)
            
  
        

 
# Column을 추가할 수 있도록 xml_string1을 업데이트합니다.
 