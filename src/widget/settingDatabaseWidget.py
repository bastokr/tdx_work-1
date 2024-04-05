import sys
from PyQt5.QtWidgets import *
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QVBoxLayout, QHBoxLayout
from PyQt5.QtCore import pyqtSignal, QObject

from lib.CRUD import CRUD
import lib.Databases as Databases

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
        self.textEdit = QLineEdit()

        label1_2 = QLabel("속성:")
        self.textEdit1_2 = QLineEdit()

        label2 = QLabel("타입:")
        self.spinBox = QSpinBox()
        label3 = QLabel("Boolean  :")
        self.checkBox = QCheckBox()

        label4 = QLabel("Options  :") 
        self.comboBox = QComboBox()
        self.comboBox.addItems(["Option 1", "Option 2", "Option 3"])
        
        
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
        groupBoxLayout.addWidget(self.textEdit)
        groupBoxLayout.addWidget(label1_2)
        groupBoxLayout.addWidget(self.textEdit1_2)
        groupBoxLayout.addWidget(label2)
        groupBoxLayout.addWidget(self.spinBox)
        groupBoxLayout.addWidget(label3)
        groupBoxLayout.addWidget(self.checkBox)
        groupBoxLayout.addWidget(label4)
        groupBoxLayout.addWidget(self.comboBox) 
        
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
        db = CRUD() 
        result = db.insertDB( table="tdx_table",)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = SettingDatabaseWidget()
    window.setWindowTitle("Setting Database Widget")
    window.setGeometry(100, 100, 400, 300)
    window.show()
    sys.exit(app.exec_())
