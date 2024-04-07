from PyQt5.QtWidgets import *  
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QWidget
from PyQt5.QtWidgets import *

from lib.CRUD import CRUD
 

class MainList(QWidget):
    def __init__(self):
        super().__init__() 
        self.setupUI()

    def setupUI(self):
        self.tableWidget = QTableWidget()
        #self.tableWidget.setRowCount(0)
        self.tableWidget.setColumnCount(4)

        self.tableWidget.setEditTriggers(QAbstractItemView.NoEditTriggers)
        # self.tableWidget.setEditTriggers(QAbstractItemView.DoubleClicked)
        # self.tableWidget.setEditTriggers(QAbstractItemView.AllEditTriggers)
        
        self.tableWidget.setHorizontalHeaderLabels(["id", "테이브id","컬럼명","타입"])  
        self.tableWidget.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        #self.tableWidget.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeToContents)

        #for i in range(20):
        #    for j in range(4):
        #        self.tableWidget.setItem(i, j, QTableWidgetItem(str(i+j)))

        layout = QVBoxLayout()
        self.label1 = QLabel("테이블명:")
        self.textEdit = QLineEdit()
        
        layout.addWidget(self.label1)
        layout.addWidget(self.tableWidget)
        self.setLayout(layout)

        self.setWindowTitle('QTableWidget')
    
    def message(self,o: object, y: str,z:str):
        print(o)    
        print(y)  
        self.label1.setText('테이블:'+y)
        print(z) 
        self.gridinit( o)
     
 
    def gridinit(self,o:object):
        db = CRUD() 
        self.result = db.whereDB( table="tdx_column", colum="*" , where ="table_id='"+str(o)+"'")
        i =0
        #result.count
        self.tableWidget.setRowCount(len(self.result))
        
        
        for i, data in enumerate(self.result):
            for j, value in enumerate(data):
                item = QTableWidgetItem(str(value))
                self.tableWidget.setItem(i, j, item)
    
        
    
    # https://freeprog.tistory.com/333 샘플 소스     
        