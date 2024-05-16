import sys
import os

# 현재 파일의 절대 경로를 가져옴
current_dir = os.path.dirname(os.path.abspath(__file__))

# src 디렉토리를 sys.path에 추가
sys.path.append(current_dir)

# PyQt5 및 기타 모듈 임포트
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

    def default_param(self, id):
        self.codeView.default_param(id)

        db = CRUD()
        self.id = id
        self.result = db.whereDB(table="tdx_query_param", colum="*", where=f"tdx_query_id='{str(id)}'")
        i = 0
        # result.count


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = Sapui5MainList()
    window.show()
    sys.exit(app.exec_())
