import sys
from PyQt5.QtWidgets import *
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QVBoxLayout, QHBoxLayout
from PyQt5.QtCore import pyqtSignal, QObject

from lib.crud import Crud
import lib.databases as Databases

class SettingDatabaseWidget(QDialog):
    closeDialog = pyqtSignal() # type: ignore

    def __init__(self):
        super().__init__()

        self.setupUI()
 
    def setupUI(self):
        groupBox = QGroupBox("Properties Data")
        groupBoxLayout = QVBoxLayout()
        
        # Add different types of input widgets
        label1 = QLabel("테이블명:")
        self.tableId = QLineEdit()

        label1_2 = QLabel("속성:")
        self.tableName = QLineEdit()

        label2 = QLabel("설명:")
        self.textDescription = QLineEdit() 
         
        btn1 = QPushButton('&테이블생성', self)
        btn1.setCheckable(True)
        btn1.toggle()
        btn1.setFixedSize(100, 30)  # Set fixed size for the button
        btn1.clicked.connect(self.addTable)

        btn2 = QPushButton(self)
        btn2.setText('닫기&2')
        btn2.setFixedSize(100, 30)  # Set fixed size for the button
        btn2.clicked.connect(self.close_dialog)  # Connect clicked signal to close_popup_window method

        hbox = QHBoxLayout() 
        hbox.addStretch(1)  # Add stretch to center align buttons
        hbox.addWidget(btn1)
        hbox.addWidget(btn2)
        hbox.addStretch(1)  # Add stretch to center align buttons

        groupBoxLayout.addWidget(label1)
        groupBoxLayout.addWidget(self.tableId)
        groupBoxLayout.addWidget(label1_2)
        groupBoxLayout.addWidget(self.tableName)
        groupBoxLayout.addWidget(label2)
        groupBoxLayout.addWidget(self.textDescription) 
        
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
        table_id = self.tableId.text()
        table_name = self.tableName.text()
        description = self.textDescription.text()

        if not table_id:
            QMessageBox.about(self, 'About Title', 'Table ID cannot be empty.')
            return

        db = Crud()
        db.insertDB( table="tdx_table", 
                    colum="id, name, description",data=(table_id, table_name, description))
    

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = SettingDatabaseWidget()
    window.setWindowTitle("Setting Database Widget")
    window.setGeometry(100, 100, 400, 300)
    window.show()
    sys.exit(app.exec_())
