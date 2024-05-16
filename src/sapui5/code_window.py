import html
import os
import sys
from turtle import width
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QTextEdit, QPushButton
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont
import xml.etree.ElementTree as ET
import xml.dom.minidom

from lib.crud import Crud


class CodeWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("PyQt5 Code Viewer and Executor")
        self.setGeometry(100, 100, 800, 600)

        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        self.layout = QVBoxLayout()
        self.central_widget.setLayout(self.layout)

        self.code_editor = QTextEdit()
        #self.code_editor.setFont(QFont("Courier", 10))
        self.code_editor.setTabStopDistance(20)
        #self.code_editor.()
         
        NS_root = 'https://yys630.tistory.com/'
        NS_data = 'https://yys630.tistory.com/data'
        ET.register_namespace('root', NS_root)
        ET.register_namespace('dt', NS_data)
        Root = ET.Element('{%s}Root' % NS_root)
        Data = ET.SubElement(Root, '{%s}Data' % NS_data)
        Data.attrib['Young'] = 'Rich'
        Subdata = ET.SubElement(Data, '{%s}Subdata' % NS_data)
        Subdata.text = 'Always Happy'
        xml_string = ET.tostring(Root, encoding='utf-8', method='xml')
        print(xml_string.decode('utf-8'))
        file_path = 'grid.xml'
        current_directory = os.path.dirname(os.path.realpath(__file__))

        
        with open(current_directory+"/"+file_path,'r') as file:
            self.file_content = file.read() 

        self.code_editor.setText(self.file_content)
        
 
        self.layout.addWidget(self.code_editor)

        self.execute_button = QPushButton("Execute")
        self.execute_button.clicked.connect(self.execute_code)
        self.layout.addWidget(self.execute_button, alignment=Qt.AlignRight)
        
    
    def default_param(self,id):
        
        db = Crud()
        self.id = id; 
        self.result , colnames = db.whereDB( table="tdx_query_param", column="*" , where ="tdx_query_id='"+id+"'",return_column_names=True)
        i =0
      #result.count
        
        for i, data in enumerate(self.result):
            print(data[2])
            #self.add_parameter(data[2], data[1])
            
            colm = '''<Column width="11rem">
						<m:Label text="Product Name" />
						<template>
							<m:Text text="{ }" wrapping="false" />
						</template>
                    </Column>''' 
                    
            self.file_content = self.file_content.replace("[columnData]", colm)
            self.code_editor.setText(self.file_content)


                

    
        
         

    def execute_code(self):
        code = self.code_editor.toPlainText()
        
        try:
            exec(code)
        except Exception as e:
            print("An error occurred:", e)
            
  
        

 
# Column을 추가할 수 있도록 xml_string1을 업데이트합니다.
 