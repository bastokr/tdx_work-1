from PyQt5.QtWidgets import *
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import pyqtSignal 

import psycopg2

from dio.query import Query
from lib.crud import Crud
import lib.databases as Databases

class Sapui5LeftTree(QWidget):

    attributeChange = pyqtSignal(int, str, str)
    attributeQuery = pyqtSignal(Query)

    def __init__(self):
        super().__init__()
        self.db = Crud()  # Initialize Crud object
        self.setupUI()

    def setupUI(self):
        layout = QVBoxLayout(self)
        self.tree = QTreeWidget(self)
        self.tree.setColumnCount(4)
        self.tree.setColumnWidth(0, 250)
        self.tree.setHeaderLabels(["구분", "속성", "id", "구분"])

        itemTable = QTreeWidgetItem(self.tree)
        itemTable.setText(0, "테이블")

        itemQuery = QTreeWidgetItem(self.tree)
        itemQuery.setText(0, "쿼리")

        self.tree.itemClicked.connect(self.onItemClicked)
        self.refresh_data()  # Load data from the database

        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setWidget(self.tree)
        layout.addWidget(scroll_area)
        self.setLayout(layout)

    def refresh_data(self):
        self.tree.clear()
        itemTable = QTreeWidgetItem(self.tree)
        itemTable.setText(0, "테이블")

        itemQuery = QTreeWidgetItem(self.tree)
        itemQuery.setText(0, "쿼리")

        if not self.db.cursor:
            return

        tables = self.db.readDB(table="tdx_table", column="*")
        for data in tables:
            child = QTreeWidgetItem(itemTable)
            child.setText(0, data[1])
            child.setText(1, data[2])
            child.setText(2, str(data[0]))
            child.setText(3, "table")

        queries = self.db.readDB(table="tdx_query", column="*")
        for data in queries:
            child = QTreeWidgetItem(itemQuery)
            child.setText(0, data[2])
            child.setText(1, data[1])
            child.setText(2, str(data[0]))
            child.setText(3, "query")

    @QtCore.pyqtSlot(QtWidgets.QTreeWidgetItem, int)
    def onItemClicked(self, it, col):
        print("클릭된 아이템:", it, "열:", col, "값:", it.text(col))
        itemType = it.text(3)  # 'table' 또는 'query' 값을 가집니다.
        if itemType == 'table':
            self.attributeChange.emit(int(it.text(2)), it.text(0), it.text(1))
        elif itemType == 'query':
            query_id = int(it.text(2))
            query = Query(id=query_id, http_request=it.text(1), odata_query_name=it.text(0), query=it.text(3), title=it.text(4))
            self.attributeQuery.emit(query)

