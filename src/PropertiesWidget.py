import sys
from PyQt5.QtWidgets import * 
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon
class PropertiesWidget(QWidget):
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

        label5 = QLabel("label5")  
        label6 = QLabel("label6")  
        label7 = QLabel("label7")    
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
        groupBoxLayout.addWidget(label5) 
        groupBoxLayout.addWidget(label6) 
        groupBoxLayout.addWidget(label7) 
        groupBoxLayout.addStretch(1) 


        groupBox.setLayout(groupBoxLayout)

        layout = QVBoxLayout()
        layout.addWidget(groupBox)
        self.setLayout(layout)
    def message(self,o: object, y: str,z:str):
        print(o)    
        print(y)  
        self.textEdit1_2.setText(z)
        print(z) 
 