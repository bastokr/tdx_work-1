import sys
import requests
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QListWidget, QListWidgetItem, QMessageBox, QDialog
from QueryCreator import QueryCreator
from PyQt5.QtCore import Qt

class QueryViewer(QWidget):
    def __init__(self):
        super().__init__()
        self.setupUI()

    def setupUI(self):
        self.setWindowTitle("Query Viewer")
        layout = QVBoxLayout()
        self.queryList = QListWidget()
        self.queryList.itemDoubleClicked.connect(self.onItemDoubleClicked)
        self.loadQueries()
        layout.addWidget(self.queryList)
        self.setLayout(layout)

    def loadQueries(self):
        try:
            response = requests.get("http://localhost:8081/api/v1/query/all")
            if response.status_code == 200:
                queries = response.json()
                for query in queries:
                    listItem = QListWidgetItem(f"{query['title']} (ID: {query['id']})")
                    listItem.setData(Qt.UserRole, query['id'])
                    self.queryList.addItem(listItem)
            else:
                QMessageBox.critical(self, "API Error", "Failed to fetch queries from the server")
        except requests.exceptions.RequestException as e:
            QMessageBox.critical(self, "Request Error", f"An error occurred: {str(e)}")

    def onItemDoubleClicked(self, item):
        try:
            query_id = item.data(Qt.UserRole)
            self.showQueryDetails(query_id)
        except Exception as e:
            QMessageBox.critical(self, "Error", f"An unexpected error occurred: {str(e)}")

    def showQueryDetails(self, query_id):
        try:
            response = requests.get(f"http://localhost:8081/api/v1/query/{query_id}")
            if response.status_code == 200:
                query = response.json()
                editor = QueryCreator()
                if 'query' in query:  # Ensure 'query' key exists in response
                    editor.loadQuery(query)
                else:
                    QMessageBox.critical(self, "Data Error", "Query data is incomplete or incorrect")
                editor.exec_()
            else:
                QMessageBox.critical(self, "API Error", "Failed to fetch query details from the server")
        except requests.exceptions.RequestException as e:
            QMessageBox.critical(self, "Request Error", f"An error occurred: {str(e)}")
        except KeyError as e:
            QMessageBox.critical(self, "Key Error", f"Missing key: {str(e)}")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    viewer = QueryViewer()
    viewer.show()
    sys.exit(app.exec_())
