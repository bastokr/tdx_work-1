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

from PyQt5.QtWidgets import QDialog
#출처: https://spec.tistory.com/422 [Code Hunter:티스토리] 

import qdarkstyle

 

class MyWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("TDX platform v0.1")
        self.setGeometry(200, 200, 1200, 700)  # x, y, w, h 
        self.menubar = self.menuBar()
        self.menubar.setNativeMenuBar(False)
        self.setContentsMargins(0, 0, 0, 0)
        self.setWindowIcon(QIcon('src/img/web.png'))

        # file menu action
        self.new_action = QAction("New")
        self.quit_action = QAction("Quit")
        self.table_action = QAction("Table")
        self.quit_action.triggered.connect(self.close)

        # help menu action
        self.doc_action = QAction("Documentation")
        self.release_action = QAction("Release Notes")
        self.license_action = QAction("View License")

        # file menu
        file_menu = self.menubar.addMenu("DataBase")
        file_menu.addAction(self.table_action)
        file_menu.addSeparator()
        file_menu.addAction(self.quit_action)
        
        self.table_action.triggered.connect(self.dialog_open);

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
        self.home_action = QAction(QIcon("src/img/home.png"), 'home')
        self.home_action.triggered.connect(self.close)

        self.setting_action = QAction(QIcon("src/img/settings.png"), 'settings')
        self.setting_action.triggered.connect(self.setting)

        self.envelope_action = QAction(QIcon("src/img/envelope.png"), 'envelope')
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
        self.dialog = QDialog() 

    # 버튼 이벤트 함수
    def dialog_open(self):
        # 버튼 추가
        btnDialog = QPushButton("OK", self.dialog)
        btnDialog.move(100, 100)
        btnDialog.clicked.connect(self.dialog_close)

        # QDialog 세팅
        self.dialog.setWindowTitle('Dialog')
        self.dialog.setWindowModality(Qt.ApplicationModal)
        self.dialog.resize(300, 200)
        self.dialog.show()

    # Dialog 닫기 이벤트
    def dialog_close(self):
        self.dialog.close()

#출처: https://spec.tistory.com/422 [Code Hunter:티스토리]
 

    def mousePressEvent(self, e): 
        print("mousePressEvent")
         

    def setting(self):
        print('setting toolbar clicked')

    def envelope(self):
        print('envelope toolbar clicked')
        
        # About 버튼 클릭 이벤트
    def About_event(self) :
        QMessageBox.about(self,'About Title','About Message')
#출처: https://mr-doosun.tistory.com/29 [고졸 입니다만..:티스토리]

if __name__ == "__main__":
    app = QApplication(sys.argv)

    app.setStyle("Fusion")
    palette = QPalette()
    palette.setColor(QPalette.HighlightedText, Qt.black)
    app.setPalette(palette)
    app.setStyleSheet(qdarkstyle.load_stylesheet(qt_api='pyqt5'))

    window = MyWindow()
    window.show()
    sys.exit(app.exec_())