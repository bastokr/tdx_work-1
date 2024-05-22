import sys
from PyQt5.QtWidgets import *
from PyQt5.QtGui import QIcon, QPalette
from PyQt5.QtCore import Qt
import configparser

from dio.query import Query
from sapui5.query_creator import SapUIQueryCreator
from sapui5.sapui5_left_tree import Sapui5LeftTree
from sapui5.sapui5_main_list import Sapui5MainList
from widget.properties_widget import PropertiesWidget
from left_tree import LeftTree
from main_list import MainList
from query_view import QueryView
from query_viewer import QueryViewer
from widget.make_dynamic_table_widget import MakeDynamicTableWidget
from query_creator import QueryCreator
from widget.database_setting_widget import DatabaseSettingWidget
from lib.crud import Crud
from pyqttoast import Toast, ToastPreset
from tab_widget import TabWidget

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("TDX platform v1.0")
        self.setGeometry(200, 200, 1200, 700)  # x, y, w, h
        self.menubar = self.menuBar()
        self.menubar.setNativeMenuBar(False)
        self.setContentsMargins(0, 0, 0, 0)
        self.setWindowIcon(QIcon('src/img/web.png'))

        self.db_settings = {}
        self.load_db_config()
        self.db = Crud()
        if self.db_settings:
            self.db.set_settings(self.db_settings)

        self.lefttree = LeftTree()
        self.main = MainList()
        self.properties_widget = PropertiesWidget()

        self.setupUI()

    def setupUI(self):
        main_layout = QVBoxLayout()
        hbox_layout = QHBoxLayout()
        tab_widget = TabWidget()
        
        hbox_layout.addWidget(self.lefttree)
        hbox_layout.addWidget(self.main)
        hbox_layout.addWidget(self.properties_widget)

        main_layout.addLayout(hbox_layout)
        main_layout.addWidget(tab_widget)

        central_widget = QWidget()
        central_widget.setLayout(main_layout)
        self.setCentralWidget(central_widget)

        self.lefttree.attributeChange.connect(self.properties_widget.message)
        self.lefttree.attributeChange.connect(self.main.message)

        self.menubar = self.menuBar()
        self.menubar.setNativeMenuBar(False)
        self.setContentsMargins(0, 0, 0, 0)

        # file menu action 
        self.sapui5_action = QAction("sapui5")
        self.sapui5_action.triggered.connect(self.showSapui5Viewer)

        self.quit_action = QAction("Quit")
        self.quit_action.triggered.connect(self.close)
        
        self.table_action = QAction("메인화면")
        self.table_action.triggered.connect(self.dialog_table_create_open)

        self.db_settings_action = QAction("DB 설정")
        self.db_settings_action.triggered.connect(self.show_db_settings_dialog)


        self.table_action = QAction("테이블생성")
        self.table_action.triggered.connect(self.dialog_table_create_open)
        
        self.table_mgt_action = QAction("테이블관리")
        self.table_mgt_action.triggered.connect(self.showTableParameters)
        # file menu
        database_menu = self.menubar.addMenu("DataBase")
        
        database_menu.addAction(self.db_settings_action)
        database_menu.addSeparator()

        database_menu.addAction(self.table_action)  
        database_menu.addSeparator()
        database_menu.addAction(self.table_mgt_action)
        
        database_menu.addSeparator()
        database_menu.addAction(self.quit_action)
 
        database_menu = self.menubar.addMenu("SAPUI5")
        database_menu.addAction(self.sapui5_action) 

        
        # help menu
        help_menu = self.menubar.addMenu("Help")  
        self.home_action = QAction(QIcon("src/img/home.png"), 'home')
        self.home_action.triggered.connect(self.home)

        self.setting_action = QAction(QIcon("src/img/settings.png"), 'settings')
        self.setting_action.triggered.connect(self.setting)

        self.envelope_action = QAction(QIcon("src/img/envelope.png"), 'envelope')
        self.envelope_action.triggered.connect(self.envelope)

        self.toolbar = self.addToolBar('title')
        self.toolbar.addAction(self.home_action)
        self.toolbar.addSeparator()
        self.toolbar.addAction(self.setting_action)
        self.toolbar.addAction(self.envelope_action)
 
        self.table_action.triggered.connect(self.dialog_table_create_open)

        self.lefttree.attributeChange.connect(self.showTableDetails)
        self.lefttree.attributeQuery.connect(self.showQueryParameters)

    def showTableParameters(self ):
        try: 

            self.splitter.replaceWidget(1, self.lefttree)
            self.splitter.replaceWidget(1, self.main)
            self.splitter.replaceWidget(2, self.properties_widget)  
        except Exception as e:   
            QMessageBox.critical(self, "오류", f"쿼리 파라미터를 로드하는 중 오류가 발생했습니다: {str(e)}")

   

    def showTableDetails(self, table_id, table_name, _):
        if not hasattr(self, 'mainList'):
            self.mainList = MainList()
        self.mainList.message(table_id, table_name, _)
        self.splitter.replaceWidget(1, self.mainList)

    def showQueryDetails(self, query_id, query_name, _):
        self.queryViewer = QueryView()
        self.queryViewer.showQueryDetails(query_id)
        self.splitter.replaceWidget(1, self.queryViewer)

    def showQueryParameters(self, query: Query):
        try:
            self.queryview = QueryView()
            self.queryCreator = QueryCreator()
            self.splitter.replaceWidget(1, self.queryview)
            self.splitter.replaceWidget(2, self.queryCreator)
            self.queryview.message(query)
            self.queryCreator.default_param(query.id)
        except Exception as e:   
            QMessageBox.critical(self, "오류", f"쿼리 파라미터를 로드하는 중 오류가 발생했습니다: {str(e)}")

    def showSapui5Viewer(self, query: Query):
        try:
            self.sapui5leftTabView = Sapui5LeftTree()
            self.sapui5MainView = Sapui5MainList()
 
            self.sapui5leftTabView.attributeChange.connect(self.showSapUIQueryParameters)
            self.sapui5leftTabView.attributeQuery.connect(self.showSapUIQueryParameters)
            self.queryCreator = SapUIQueryCreator()
         

            self.splitter.replaceWidget(0, self.sapui5leftTabView)
            self.splitter.replaceWidget(1, self.sapui5MainView)
            self.splitter.replaceWidget(2, self.queryCreator)
            
            self.queryCreator.replaceGrid.connect(self.sapui5MainView.showGrid)
            #self.queryCreator.default_param(query.id)
            
             
        except Exception as e:
            QMessageBox.critical(self, "오류", f"쿼리 파라미터를 로드하는 중 오류가 발생했습니다: {str(e)}")

    def showSapUIQueryParameters(self, query: Query):
        try:
            self.sapui5MainView.default_param(query.id) 
            self.queryCreator.default_param(query.id)
        except Exception as e:
            QMessageBox.critical(self, "오류", f"쿼리 파라미터를 로드하는 중 오류가 발생했습니다: {str(e)}")

    def dialog_table_create_open(self):
        self.dialog = QDialog()
        self.dialog.setWindowTitle('My Dialog')
        layout = QHBoxLayout(self.dialog)

        preview = QLabel('', self.dialog)
        setting = MakeDynamicTableWidget()
        layout.addWidget(setting)
        self.dialog.setWindowModality(Qt.ApplicationModal)
        self.dialog.resize(800, 500)
        setting.closeDialog.connect(self.dialog.close)
        self.dialog.show()

    def dialog_close(self):
        self.dialog.close()

    def mousePressEvent(self, e):
        print("mousePressEvent")

    def setting(self):
        print('setting toolbar clicked')
    
    

    def home(self):
        print('setting toolbar clicked')
        self.showTableParameters()

    def envelope(self):
        print('envelope toolbar clicked')

    def About_event(self):
        QMessageBox.about(self, 'About Title', 'About Message')

    def open_query_creator(self):
        dialog = QueryCreator(self)
        dialog.show()

    def show_db_settings_dialog(self):
        db_settings_dialog = DatabaseSettingWidget()
        db_settings_dialog.closeDialog.connect(self.save_db_settings)
        db_settings_dialog.exec_()

    def save_db_settings(self, settings):
        config = configparser.ConfigParser()
        config['Database'] = settings
        with open('config.ini', 'w') as configfile:
            config.write(configfile)
        self.db.set_settings(settings)
    
        # Show a custom Snackbar instead of a QMessageBox
        self.show_toast("TDX message","Database settings saved successfully.")  # Create a Snackbar instance
         
        self.lefttree.db.set_settings(settings)  # LeftTree에 데이터베이스 설정 전달
        self.lefttree.refresh_data()  # 데이터베이스 설정 후 데이터를 갱신
    
        # Shows a toast notification every time the button is clicked
    def show_toast(self,title,message):
        toast = Toast(self)
        toast.setDuration(2000)  # Hide after 5 seconds
        toast.setTitle(title)
        toast.setText(message)
        toast.applyPreset(ToastPreset.SUCCESS)  # Apply style preset
        toast.show()

    def load_db_config(self):
        import os
        

        # 현재 스크립트의 디렉토리 가져오기
        script_dir = os.path.dirname(os.path.abspath(__file__))
        # config.ini 파일의 절대 경로 생성
        config_path = os.path.join(script_dir, 'config.ini')
        abs_config_path = os.path.abspath(config_path)
        print(f"Loading configuration from: {abs_config_path}")

        if not os.path.exists(abs_config_path):
            print("Configuration file does not exist.")
            return

        config = configparser.ConfigParser()
        config.read(abs_config_path)

        print("Configuration file content:")
        with open(abs_config_path, 'r') as f:
            print(f.read())

        if 'Database' in config:
            print('config.ini 파일 기반 데이터베이스 설정')
            self.db_settings = {
                'host': config.get('Database', 'host', fallback=''),
                'dbname': config.get('Database', 'dbname', fallback=''),
                'user': config.get('Database', 'user', fallback=''),
                'password': config.get('Database', 'password', fallback=''),
                'port': config.get('Database', 'port', fallback='')
            }
        else:
            print('Database 설정이 없습니다.')

class MyApp(QApplication):
    def applicationSupportsSecureRestorableState(self):
        return True


if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setStyle("Fusion")
    palette = QPalette()
    app.setPalette(palette)

    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
