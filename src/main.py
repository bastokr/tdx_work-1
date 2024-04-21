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

from query_view import QueryView  

from PyQt5.QtWidgets import QDialog


#import qdarkstyle

from widget.settingDatabaseWidget import SettingDatabaseWidget

 

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

        # 쿼리 생성 메뉴 항목 추가
        query_menu = self.menubar.addMenu("Query")
        create_query_action = QAction("Create Query", self)
        query_menu.addAction(create_query_action)
        create_query_action.triggered.connect(self.create_query_popup)

        # Create buttons 
        #btn2 = QPushButton("Button2")

        # Create custom widget
       
        self.lefttree = LeftTree()
        self.main = MainList()
  
        # Setting up central widget and layout
        central_widget = QWidget()

        central_widget.setContentsMargins(0,0,0,0)
        self.splitter = QSplitter(Qt.Horizontal)  # Use Qt namespace from QtCore
        #left_widget = QTextEdit()
        right_widget = QLabel("Layer 2")
        self.lefttree.setGeometry(0,0,100,1000)  
         
        self.splitter.addWidget(self.lefttree)
        
        self.splitter.addWidget(self.main)
       


        self.setCentralWidget(self.splitter)
        self.properties_widget = PropertiesWidget()

        self.splitter.addWidget(self.properties_widget)

        self.lefttree.attributeChange.connect( self.properties_widget.message   )
        self.lefttree.attributeChange.connect(self.main.message)
        
        self.lefttree.attributeQuery.connect(self.changeQueryTab)

    
    def changeQueryTab(self,table_id: object, table_nm: str,z:str):
        print(table_id)
        self.queryView = QueryView();
        #query_widget = self.splitter.widget(1)
        self.splitter.replaceWidget(1,self.queryView)
        #old_widget.deleteLater()
        
        
       
        
        
        
     

    # 버튼 이벤트 함수
    def dialog_open(self):
        self.dialog  = QDialog()
        self.dialog.setWindowTitle('My Dialog')
        layout = QHBoxLayout(self.dialog ) 
        
        preview = QLabel('', self.dialog )
        setting = SettingDatabaseWidget()
        layout.addWidget(setting) 
        self.dialog.setWindowModality(Qt.ApplicationModal)
        self.dialog.resize(800, 500)
        setting.closeDialog.connect(self.dialog.close)
        self.dialog.show()
        
        

    # Dialog 닫기 이벤트
    def dialog_close(self):
        self.dialog.close()

 

    def mousePressEvent(self, e): 
        print("mousePressEvent")
         

    def setting(self):
        print('setting toolbar clicked')

    def envelope(self):
        print('envelope toolbar clicked')
        
        # About 버튼 클릭 이벤트
    def About_event(self) :
        QMessageBox.about(self,'About Title','About Message')

    def create_query_popup(self):
        # Dialog setup
        self.query_dialog = QDialog(self)
        self.query_dialog.setWindowTitle("Create Query")
        layout = QVBoxLayout(self.query_dialog)

        # 쿼리 이름 입력
        layout.addWidget(QLabel("Name:"))
        self.query_name_input = QLineEdit()
        layout.addWidget(self.query_name_input)

        # SQL 쿼리 입력
        layout.addWidget(QLabel("SQL Query:"))
        self.query_input = QTextEdit()
        self.query_input.setFixedHeight(100)  # 적당한 높이 설정
        layout.addWidget(self.query_input)

        # 매개변수 테이블
        self.params_table = QTableWidget(0, 3)
        self.params_table.setHorizontalHeaderLabels(['Name', 'Data Type', 'Value'])
        layout.addWidget(self.params_table)

        # 매개변수 추가 버튼
        add_param_btn = QPushButton('Add Parameter')
        add_param_btn.clicked.connect(self.add_parameter)
        layout.addWidget(add_param_btn)

        # 저장 버튼
        save_query_btn = QPushButton('Save Query')
        save_query_btn.clicked.connect(self.save_query)
        layout.addWidget(save_query_btn)

        self.query_dialog.setLayout(layout)
        self.query_dialog.exec_()

    def add_parameter(self):
        row_count = self.params_table.rowCount()
        self.params_table.insertRow(row_count)
        self.params_table.setItem(row_count, 0, QTableWidgetItem(""))  # Name
        self.params_table.setItem(row_count, 1, QTableWidgetItem(""))  # Data Type
        self.params_table.setItem(row_count, 2, QTableWidgetItem(""))  # Value

    def save_query_to_db(self):
        query_text = self.query_input.text()
        # 쿼리 저장 로직을 여기에 구현
        # ...
        print("Query saved:", query_text)
        self.dialog.accept()

    def save_query(self):
        query_name = self.query_name_input.text()
        query_text = self.query_input.toPlainText()
        parameters = []
        for row in range(self.params_table.rowCount()):
            name = self.params_table.item(row, 0).text()
            data_type = self.params_table.item(row, 1).text()
            value = self.params_table.item(row, 2).text()
            parameters.append((name, data_type, value))
        # 데이터베이스에 쿼리 및 매개변수 저장 로직 구현
        print("Name:", query_name)
        print("Query:", query_text)
        print("Parameters:", parameters)
        self.query_dialog.accept()


if __name__ == "__main__":
    app = QApplication(sys.argv)

    app.setStyle("Fusion")
    palette = QPalette()
    #palette.setColor(QPalette.HighlightedText, Qt.black)
    app.setPalette(palette)
    #app.setStyleSheet(qdarkstyle.load_stylesheet(qt_api='pyqt5'))

    window = MyWindow()
    window.show()
    sys.exit(app.exec_())