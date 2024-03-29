import sys
from PyQt5.QtWidgets import * 
from PyQt5.QtGui import QIcon, QPalette, QColor
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QWidget
from PyQt5.QtWidgets import *
 
from PropertiesWidget import PropertiesWidget
from lefttree import LeftTree 
from PyQt5.QtCore import pyqtSignal, QObject

from main_view import MainList

 
 

class MyWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("TDX platform v0.1")
        self.setGeometry(200, 200, 1200, 700)  # x, y, w, h 
        self.menubar = self.menuBar()
        self.menubar.setNativeMenuBar(False)
        self.setContentsMargins(0, 0, 0, 0)
        self.setWindowIcon(QIcon('web.png'))

        # file menu action
        self.new_action = QAction("New")
        self.quit_action = QAction("Quit")
        self.quit_action.triggered.connect(self.close)

        # help menu action
        self.doc_action = QAction("Documentation")
        self.release_action = QAction("Release Notes")
        self.license_action = QAction("View License")

        # file menu
        file_menu = self.menubar.addMenu("File")
        file_menu.addAction(self.new_action)
        file_menu.addSeparator()
        file_menu.addAction(self.quit_action)

        file_menu = self.menubar.addMenu("Edit")
        file_menu.addAction(self.new_action)
        file_menu.addSeparator()
        file_menu.addAction(self.quit_action)

        
        file_menu = self.menubar.addMenu("Selection")
        file_menu.addAction(self.new_action)
        file_menu.addSeparator()
        file_menu.addAction(self.quit_action)
        
        file_menu = self.menubar.addMenu("View")
        file_menu.addAction(self.new_action)
        file_menu.addSeparator()
        file_menu.addAction(self.quit_action)
        

        file_menu = self.menubar.addMenu("oData")
        file_menu.addAction(self.new_action)
        file_menu.addSeparator()
        file_menu.addAction(self.quit_action)


        file_menu = self.menubar.addMenu("Make")
        file_menu.addAction(self.new_action)
        file_menu.addSeparator()
        file_menu.addAction(self.quit_action)

        file_menu = self.menubar.addMenu("Run")
        file_menu.addAction(self.new_action)
        file_menu.addSeparator()
        file_menu.addAction(self.quit_action)
 
        # help menu
        help_menu = self.menubar.addMenu("Help")
        help_menu.addAction(self.doc_action)
        help_menu.addAction(self.release_action)
        help_menu.addAction(self.license_action)
        self.home_action = QAction(QIcon("home.png"), 'home')
        self.home_action.triggered.connect(self.close)

        self.setting_action = QAction(QIcon("settings.png"), 'settings')
        self.setting_action.triggered.connect(self.setting)

        self.envelope_action = QAction(QIcon("envelope.png"), 'envelope')
        self.envelope_action.triggered.connect(self.envelope)

        self.toolbar = self.addToolBar('title')
        self.toolbar.addAction(self.home_action)
        self.toolbar.addSeparator()
        self.toolbar.addAction(self.setting_action)
        self.toolbar.addAction(self.envelope_action)

        # Create buttons 
        #btn2 = QPushButton("Button2")

        # Create custom widget
       
        self.lefttree = LeftTree()
        self.main = MainList()
  
        # Setting up central widget and layout
        central_widget = QWidget()

        central_widget.setContentsMargins(0,0,0,0)
        splitter = QSplitter(Qt.Horizontal)  # Use Qt namespace from QtCore
        #left_widget = QTextEdit()
        right_widget = QLabel("Layer 2")
        self.lefttree.setGeometry(0,0,100,1000)  
         
        splitter.addWidget(self.lefttree)
        
        splitter.addWidget(self.main)
       


        self.setCentralWidget(splitter)
        self.properties_widget = PropertiesWidget()

        splitter.addWidget(self.properties_widget)

        self.lefttree.attributeChange.connect( self.properties_widget.message   )

 
 

    def mousePressEvent(self, e): 
        print("mousePressEvent")
         

    def setting(self):
        print('setting toolbar clicked')

    def envelope(self):
        print('envelope toolbar clicked')

if __name__ == "__main__":
    app = QApplication(sys.argv)

    app.setStyle("Fusion")
    palette = QPalette()
    palette.setColor(QPalette.HighlightedText, Qt.black)
    app.setPalette(palette)

    window = MyWindow()
    window.show()
    sys.exit(app.exec_())