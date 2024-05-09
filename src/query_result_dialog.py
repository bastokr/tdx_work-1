from PyQt5.QtWidgets import QDialog, QVBoxLayout, QLabel, QTableWidget, QTableWidgetItem


class QueryResultDialog(QDialog):
    def __init__(self, query_results, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Query Test Results")
        self.setFixedSize(800, 600)
        layout = QVBoxLayout()

        self.result_table = QTableWidget()
        layout.addWidget(QLabel("Results:"))
        self.result_table.setColumnCount(len(query_results[0]) if query_results else 0)
        self.result_table.setRowCount(len(query_results))
        self.result_table.setHorizontalHeaderLabels([f"Column {i + 1}" for i in range(len(query_results[0]))] if query_results else [])

        for row_idx, row in enumerate(query_results):
            for col_idx, item in enumerate(row):
                self.result_table.setItem(row_idx, col_idx, QTableWidgetItem(str(item)))

        layout.addWidget(self.result_table)
        self.setLayout(layout)
