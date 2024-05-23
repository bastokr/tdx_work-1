import sys
import os

from sapui5.grid_window import GridWindow

# 현재 파일의 절대 경로를 가져옴
current_dir = os.path.dirname(os.path.abspath(__file__))

# src 디렉토리를 sys.path에 추가
sys.path.append(current_dir)

# PyQt5 및 기타 모듈 임포트
from PyQt5.QtWidgets import QApplication, QWidget, QTabWidget, QVBoxLayout
from lib.crud import Crud
from sapui5.web_view import WebView
from sapui5.code_window import CodeWindow


class Sapui5MainList(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.webView = WebView()
        self.codeView = CodeWindow()
        self.gridView = GridWindow()

        self.webView.show()

        tabs = QTabWidget()
        tabs.addTab(self.gridView, '테이블')
        #tabs.addTab(self.webView, 'Tab1')
        tabs.addTab(self.codeView, 'xml')
        tabs.addTab(self.webView, 'webView')

        vbox = QVBoxLayout()
        vbox.addWidget(tabs)

        self.setLayout(vbox)

        self.setWindowTitle('QTabWidget')
        self.setGeometry(300, 300, 300, 200)
        self.show()

    def default_param(self, id):
        self.codeView.default_param(id)
        self.gridView.default_param(id)

        db = Crud()
        self.id = id
        self.result = db.whereDB(table="tdx_query_param", column="*", where=f"tdx_query_id='{str(id)}'")
        i = 0
        # result.count
        
    def showGrid(self,str):
        self.gridView.showGrid(str)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = Sapui5MainList()
    window.show()
    sys.exit(app.exec_())
