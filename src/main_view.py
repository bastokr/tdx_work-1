from PyQt5.QtWidgets import *  
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QWidget
from PyQt5.QtWidgets import *
 

class MainList(QWidget):
    def __init__(self):
        super().__init__() 
        self.setupUI()

    def setupUI(self):
        self.tableWidget = QTableWidget()
        self.tableWidget.setRowCount(20)
        self.tableWidget.setColumnCount(4)

        self.tableWidget.setEditTriggers(QAbstractItemView.NoEditTriggers)
        # self.tableWidget.setEditTriggers(QAbstractItemView.DoubleClicked)
        # self.tableWidget.setEditTriggers(QAbstractItemView.AllEditTriggers)
        
        self.tableWidget.setHorizontalHeaderLabels(["테이블명", "속성명","타입","사용여부"])  
        self.tableWidget.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        #self.tableWidget.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeToContents)

        for i in range(20):
            for j in range(4):
                self.tableWidget.setItem(i, j, QTableWidgetItem(str(i+j)))

        layout = QVBoxLayout()
        layout.addWidget(self.tableWidget)
        self.setLayout(layout)

        self.setWindowTitle('QTableWidget')
        
 
    # https://freeprog.tistory.com/333 샘플 소스     
        