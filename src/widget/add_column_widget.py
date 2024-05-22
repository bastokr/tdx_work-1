import sys
from PyQt5.QtWidgets import *
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QVBoxLayout, QHBoxLayout
from PyQt5.QtCore import pyqtSignal, QObject

from lib.crud import Crud
import lib.databases as Databases

class AddColumnWidget(QDialog):
    closeDialog = pyqtSignal() # type: ignore

    def __init__(self,table_id,table_nm):
        self.table_nm=table_nm;
        self.table_id=table_id;
        super().__init__()

        self.setupUI()
 
    def setupUI(self):
        groupBox = QGroupBox("Add Table Column")
        groupBoxLayout = QVBoxLayout()
        
        # Add different types of input widgets
        label1 = QLabel("Table Name: "+self.table_nm)
        self.tableId = QLineEdit()
        self.tableId.setText(self.table_nm)
        self.tableId.setModified(False)
        self.tableId.setReadOnly(True)
        

        column_nm = QLabel("Column Name:")
        self.column_nm = QLineEdit()

        column_type = QLabel("Type:")
        self.column_type = QLineEdit() 
         
        btn1 = QPushButton('&Add Column', self)
        btn1.setCheckable(True)
        btn1.toggle()
        btn1.setFixedSize(100, 30)  # Set fixed size for the button
        btn1.setStyleSheet("margin: 0px;")
        btn1.clicked.connect(self.addTable)

        btn2 = QPushButton(self)
        btn2.setText('Close')
        btn2.setFixedSize(100, 30)  # Set fixed size for the button
        btn2.setStyleSheet("margin: 0px;")
        btn2.clicked.connect(self.close_dialog)  # Connect clicked signal to close_popup_window method

        hbox = QHBoxLayout() 
        hbox.addStretch(1)  # Add stretch to center align buttons
        hbox.addWidget(btn1)
        hbox.addWidget(btn2)
        hbox.addStretch(1)  # Add stretch to center align buttons

        groupBoxLayout.addWidget(label1)
        groupBoxLayout.addWidget(self.tableId)
        groupBoxLayout.addWidget(column_nm)
        groupBoxLayout.addWidget(self.column_nm)
        groupBoxLayout.addWidget(column_type)
        groupBoxLayout.addWidget(self.column_type) 
        
        groupBoxLayout.addLayout(hbox)
        groupBoxLayout.addStretch(1) 

        groupBox.setLayout(groupBoxLayout)

        layout = QVBoxLayout()
        layout.addWidget(groupBox)
        self.setLayout(layout)

        # Store reference to the pop-up window instance
        self.popup_window = self
    
    def close_dialog(self):
        # Emit the closeDialog signal when the close button is clicked
        self.closeDialog.emit()
    
    def addTable(self):
        table_id = self.table_id
        column_nm = self.column_nm.text()
        column_type = self.column_type.text() 
        seq_next="nextval('tdx_column_column_id_seq')";

        if not table_id:
            QMessageBox.about(self, 'About Title', 'Table ID cannot be empty.')
            return

        db = Crud()
        db.insertDBSeq( table="tdx_column", 
                        column="table_id,name,type",seq=seq_next, data=(table_id,column_nm , column_type))
        
        self.close_dialog()
        
        
        
        