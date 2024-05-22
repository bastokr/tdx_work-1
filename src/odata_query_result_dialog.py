from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QDialog, QVBoxLayout, QLabel, QTableWidget, QTableWidgetItem

class ODataQueryResultDialog(QDialog):
    def __init__(self, odata_results, parent=None):
        super().__init__(parent)
        self.setWindowTitle("OData Query Test Results")
        self.setFixedSize(800, 600)
        layout = QVBoxLayout()

        self.result_table = QTableWidget()
        layout.addWidget(QLabel("Results:"))
        
        if odata_results:
            # Get column names from the first item in the "value" list
            column_names = odata_results[0].keys()
            self.result_table.setColumnCount(len(column_names))
            self.result_table.setHorizontalHeaderLabels(column_names)
            self.result_table.setRowCount(len(odata_results))

            # Populate the table
            for row_idx, row_data in enumerate(odata_results):
                for col_idx, (key, value) in enumerate(row_data.items()):
                    item = QTableWidgetItem(str(value))
                    item.setTextAlignment(Qt.AlignCenter)
                    self.result_table.setItem(row_idx, col_idx, item)
        
        layout.addWidget(self.result_table)
        self.setLayout(layout)
