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
        textEdit = QLineEdit()

        label1_2 = QLabel("속성:")
        textEdit1_2 = QLineEdit()

        label2 = QLabel("타입:")
        spinBox = QSpinBox()

        label3 = QLabel("Boolean  :")
        checkBox = QCheckBox()

        label4 = QLabel("Options  :") 
        comboBox = QComboBox()
        comboBox.addItems(["Option 1", "Option 2", "Option 3"])

        label5 = QLabel("label5")  
        label6 = QLabel("label6")  
        label7 = QLabel("label7")  
        




        groupBoxLayout.addWidget(label1)
        groupBoxLayout.addWidget(textEdit)
        groupBoxLayout.addWidget(label1_2)
        groupBoxLayout.addWidget(textEdit1_2)
        groupBoxLayout.addWidget(label2)
        groupBoxLayout.addWidget(spinBox)
        groupBoxLayout.addWidget(label3)
        groupBoxLayout.addWidget(checkBox)
        groupBoxLayout.addWidget(label4)
        groupBoxLayout.addWidget(comboBox)
        groupBoxLayout.addWidget(label5) 
        groupBoxLayout.addWidget(label6) 
        groupBoxLayout.addWidget(label7) 
        groupBoxLayout.addStretch(1) 


        groupBox.setLayout(groupBoxLayout)

        layout = QVBoxLayout()
        layout.addWidget(groupBox)
        self.setLayout(layout)
 