import sys
from PyQt5.QtWidgets import QApplication, QWidget, QTabWidget, QVBoxLayout

from lib.CRUD import CRUD
from sapui5.sapuiTest import WebView
from sapui5.codeWindow import CodeWindow


class Sapui5MainList(QWidget):


    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.webView = WebView()
        
        self.codeView = CodeWindow()
        
        
        self.webView.show()
        tab2 = QWidget()

        tabs = QTabWidget()
        tabs.addTab(self.webView, 'Tab1')
        tabs.addTab(self.codeView, 'Tab2')

        vbox = QVBoxLayout()
        vbox.addWidget(tabs)

        self.setLayout(vbox)

        self.setWindowTitle('QTabWidget')
        self.setGeometry(300, 300, 300, 200)
        self.show()
        
    def default_param(self,id):
        self.codeView.default_param(id)
        
        db = CRUD() 
        self.id = id; 
        self.result = db.whereDB( table="tdx_query_param", colum="*" , where ="tdx_query_id='"+str(id)+"'")
        i =0
        #result.count
           
        for i, data in enumerate(self.result):
            self.add_parameter(data[2], data[1])
        