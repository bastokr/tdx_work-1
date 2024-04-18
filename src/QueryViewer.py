from PyQt5.QtWidgets import *
from PyQt5.QtCore import Qt

class QueryViewer(QWidget):
    def __init__(self):
        super().__init__()
        self.setupUI()

    def setupUI(self):
        layout = QVBoxLayout()

        self.queryList = QListWidget()
        self.loadQueries()
        layout.addWidget(self.queryList)

        self.setLayout(layout)

    def loadQueries(self):
        # 가정: 데이터베이스 연결 및 쿼리 로드 로직
        # 임시 데이터로 쿼리 목록을 로드합니다.
        queries = [
            {"id": 3, "title": "Get Members by Email"},
            {"id": 4, "title": "Get Members Created After a Date"},
            {"id": 7, "title": "Get Members by Name and Age"},
            {"id": 8, "title": "Test dynamic query"}
        ]
        for query in queries:
            listItem = QListWidgetItem(f"{query['title']} (ID: {query['id']})")
            self.queryList.addItem(listItem)

