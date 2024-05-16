import sys
from PyQt5.QtWidgets import *
from PyQt5.QtGui import QIcon, QPalette, QColor
from PyQt5.QtCore import Qt, pyqtSignal, QObject

from dio.query import Query
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

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("TDX platform v0.1")
        self.setGeometry(200, 200, 1200, 700)  # x, y, w, h
        self.menubar = self.menuBar()
        self.menubar.setNativeMenuBar(False)
        self.setContentsMargins(0, 0, 0, 0)
        self.setWindowIcon(QIcon('src/img/web.png'))

        self.db_settings = {}

        # 데이터베이스 연결 초기화
        self.db = Crud()

        # file menu action
        self.new_action = QAction("New")
        self.new_action.triggered.connect(self.showSapui5Viewer)

        self.quit_action = QAction("Quit")
        self.quit_action.triggered.connect(self.close)

        self.table_action = QAction("Table")
        self.table_action.triggered.connect(self.dialog_open)

        self.db_settings_action = QAction("Database Settings")
        self.db_settings_action.triggered.connect(self.show_db_settings_dialog)

        # help menu action
        self.doc_action = QAction("Documentation")
        self.release_action = QAction("Release Notes")
        self.license_action = QAction("View License")

        # file menu
        file_menu = self.menubar.addMenu("DataBase")
        file_menu.addAction(self.table_action)
        file_menu.addAction(self.db_settings_action)
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

        query_menu = self.menubar.addMenu("Query")
        create_query_action = QAction("Create Query", self)
        query_menu.addAction(create_query_action)
        create_query_action.triggered.connect(self.open_query_creator)

        self.table_action.triggered.connect(self.dialog_open)

        self.lefttree = LeftTree()
        self.main = MainList()
        central_widget = QWidget()
        central_widget.setContentsMargins(0, 0, 0, 0)
        self.splitter = QSplitter(Qt.Horizontal)
        right_widget = QLabel("Layer 2")
        self.lefttree.setGeometry(0, 0, 100, 1000)

        self.splitter.addWidget(self.lefttree)
        self.splitter.addWidget(self.main)

        self.setCentralWidget(self.splitter)
        self.properties_widget = PropertiesWidget()
        self.splitter.addWidget(self.properties_widget)

        self.lefttree.attributeChange.connect(self.properties_widget.message)
        self.lefttree.attributeChange.connect(self.main.message)

        self.setupUI()

    def setupUI(self):
        self.lefttree.attributeChange.connect(self.showTableDetails)
        self.lefttree.attributeQuery.connect(self.showQueryParameters)

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

            self.splitter.replaceWidget(0, self.sapui5leftTabView)
            self.splitter.replaceWidget(1, self.sapui5MainView)
        except Exception as e:
            QMessageBox.critical(self, "오류", f"쿼리 파라미터를 로드하는 중 오류가 발생했습니다: {str(e)}")

    def showSapUIQueryParameters(self, query: Query):
        try:
            self.sapui5MainView.default_param(query.id)
        except Exception as e:
            QMessageBox.critical(self, "오류", f"쿼리 파라미터를 로드하는 중 오류가 발생했습니다: {str(e)}")

    def dialog_open(self):
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
        self.db_settings = settings
        self.db.set_settings(settings)  # 데이터베이스 연결 설정
        QMessageBox.information(self, "Settings Saved", "Database settings saved successfully.")
        self.lefttree.refresh_data()  # 데이터베이스 설정 후 데이터를 갱신
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
