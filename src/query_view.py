from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QLineEdit, QTextEdit, QPushButton, QTableWidget, QTableWidgetItem, QHBoxLayout, QScrollArea, QComboBox, QMessageBox, QDialog
from PyQt5.QtCore import Qt
from lib.crud import Crud
from query_result_dialog import QueryResultDialog
from dio.query import Query
import requests


class QueryView(QWidget):
    def __init__(self):
        super().__init__()
        self.setupUI()
        self.parameter_widgets = []  # 매개변수 위젯을 저장하는 리스트

    def setupUI(self):
        self.setWindowTitle("Query View")
        layout = QVBoxLayout()

        layout.addWidget(QLabel("ID:"))
        self.query_id_input = QLineEdit()
        layout.addWidget(self.query_id_input)
        self.query_exp_input = QLineEdit()
        layout.addWidget(QLabel("설명:"))
        layout.addWidget(self.query_exp_input)

        layout.addWidget(QLabel("SQL Query:"))
        self.query_input = QTextEdit()
        self.query_input.setFixedHeight(200)
        layout.addWidget(self.query_input)

        self.tableWidget = QTableWidget()
        self.tableWidget.setColumnCount(5)
        self.tableWidget.setHorizontalHeaderLabels(["선택", "id", "속성", "파라미터", "value"])
        layout.addWidget(self.tableWidget)

        self.btn1 = QPushButton('&Test', self)
        self.btn1.setCheckable(True)
        self.btn1.toggle()
        self.btn1.setFixedSize(100, 30)
        self.btn1.clicked.connect(self.test_param_query)
        self.btn1.setStyleSheet("margin: 0px;")

        button_layout = QHBoxLayout()
        button_layout.addStretch(1)
        button_layout.addWidget(self.btn1)
        layout.addLayout(button_layout)

        self.btn3 = QPushButton('Register', self)
        self.btn3.setCheckable(True)
        self.btn3.toggle()
        self.btn3.setFixedSize(100, 30)
        self.btn3.clicked.connect(self.create_query_popup)
        self.btn3.setStyleSheet("margin: 0px;")
        button_layout.addWidget(self.btn3)

        layout.addLayout(button_layout)
        layout.addWidget(self.tableWidget)
        self.setLayout(layout)

    def message(self, query: Query):
        db = Crud()
        self.result = db.whereDB(table="tdx_query", column="*", where="id='" + str(query.id) + "'")
        data = self.result[0]
        self.query_id_input.setText(str(query.id))  # 쿼리 ID 값을 정확하게 설정
        self.query_exp_input.setText(data[4])
        self.query_input.setText(data[3])
        self.gridinit(query.id)

    def gridinit(self, id: object):
        db = Crud()
        self.id = id
        self.result = db.whereDB(table="tdx_query_param", column="*", where="tdx_query_id='" + str(id) + "'")
        i = 0
        self.tableWidget.setRowCount(len(self.result))

        for i, data in enumerate(self.result):
            item = checkboxItem()
            item.setFlags(Qt.ItemIsUserCheckable | Qt.ItemIsEnabled)
            item.setCheckState(Qt.CheckState.Unchecked)
            item.setData(Qt.UserRole, item.checkState())
            item.setTextAlignment(Qt.AlignCenter)
            self.tableWidget.setItem(i, 0, item)

            for j, value in enumerate(data):
                item = QTableWidgetItem(str(value))
                item.setTextAlignment(Qt.AlignCenter)
                self.tableWidget.setItem(i, j + 1, item)

        self.tableWidget.cellChanged.connect(self.onCellChanged)

    def onCellChanged(self, row, column):
        item = self.tableWidget.item(row, column)
        if item is not None:
            row_value = item.row()
            second_item = self.tableWidget.item(row_value, 3)
            if second_item is not None:
                value_of_second_item = second_item.text()
                print("Value of the second item in the row:", value_of_second_item)
            else:
                print("No second item found in the row:", row_value)
        else:
            print("No item found at row:", row, "and column:", column)

    def test_param_query(self):
        db = Crud()
        query_id = int(self.query_id_input.text())
        query_template = self.query_input.toPlainText()

        # 파라미터 가져오기
        params = {}
        query_params = db.whereDB(table="tdx_query_param", column="*", where=f"tdx_query_id={query_id}")
        for param in query_params:
            param_name = param['parameter']
            param_value = param['value']
            params[param_name] = param_value

        # 쿼리 실행
        try:
            query_results = db.execute_param_query(query_template, params)

            if query_results:
                dialog = QueryResultDialog(query_results, self)
                dialog.exec_()
            else:
                QMessageBox.information(self, "No Results", "쿼리에서 반환된 데이터가 없습니다.")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"쿼리 실행 중 오류 발생: {str(e)}")

    def create_query_popup(self):
        self.query_dialog = QDialog(self)
        self.query_dialog.setWindowTitle("Create Query")
        self.query_dialog.setFixedSize(800, 600)
        layout = QVBoxLayout()

        layout.addWidget(QLabel("Name:"))
        self.query_name_input = QLineEdit()
        layout.addWidget(self.query_name_input)

        layout.addWidget(QLabel("SQL Query:"))
        self.query_input = QTextEdit()
        self.query_input.setFixedHeight(200)
        layout.addWidget(self.query_input)

        params_container = QWidget()
        self.params_layout = QVBoxLayout(params_container)
        params_header = QHBoxLayout()
        params_header.addWidget(QLabel("Name"))
        params_header.addWidget(QLabel("Data Type"))
        params_header.addWidget(QLabel("Value"))
        layout.addLayout(params_header)

        params_scroll_area = QScrollArea()
        params_scroll_area.setWidgetResizable(True)
        params_scroll_area.setWidget(params_container)

        layout.addWidget(params_scroll_area)

        button_layout = QHBoxLayout()
        add_param_btn = QPushButton('Add Parameter')
        add_param_btn.clicked.connect(lambda: self.add_parameter("", ""))
        button_layout.addWidget(add_param_btn)
        button_layout.addStretch(1)
        layout.addLayout(button_layout)

        save_query_btn = QPushButton('Save Query')
        save_query_btn.clicked.connect(self.save_query)
        layout.addWidget(save_query_btn)

        self.query_dialog.setLayout(layout)
        self.query_dialog.exec_()

    def add_parameter(self, colname, datatype):
        param_widget = QWidget()
        param_layout = QHBoxLayout(param_widget)
        name_input = QLineEdit()
        type_input = QComboBox()
        data_types = [
            "smallint", "integer", "bigint", "decimal", "numeric", "real", "double precision", "smallserial",
            "serial", "bigserial", "char(n)", "varchar(n)", "text", "bytea", "timestamp",
            "timestamp with time zone", "date", "time with time zone", "interval", "boolean",
            "enum", "point", "line", "lseg", "box", "path", "polygon", "circle", "cidr", "inet",
            "macaddr", "macaddr8", "bit(n)", "bit varying(n)", "tsvector", "tsquery", "uuid", "xml",
            "json", "jsonb", "int4range", "int8range", "numrange", "tsrange", "daterange"
        ]
        type_input.addItems(data_types)
        value_input = QLineEdit()
        delete_btn = QPushButton("Delete")
        delete_btn.clicked.connect(lambda: self.remove_parameter(param_widget))
        param_layout.addWidget(name_input)
        param_layout.addWidget(type_input)
        param_layout.addWidget(value_input)
        param_layout.addWidget(delete_btn)

        name_input.setText(colname)
        type_input.setCurrentText(datatype)

        self.params_layout.addWidget(param_widget)
        self.parameter_widgets.append((param_widget, name_input, type_input, value_input))

    def remove_parameter(self, widget):
        widget.deleteLater()
        self.parameter_widgets = [pw for pw in self.parameter_widgets if pw[0] != widget]

    def save_query(self):
        query_name = self.query_name_input.text()
        query_text = self.query_input.toPlainText()
        parameters = []
        for _, name_input, type_input, value_input in self.parameter_widgets:
            parameters.append({
                "parameter": name_input.text(),
                "attribute": type_input.currentText(),
                "value": value_input.text()
            })
        query_data = {
            "title": query_name,
            "query": query_text,
            "parameters": parameters
        }
        url = "http://localhost:8081/api/v1/query"
        try:
            response = requests.post(url, json=query_data)
            if response.status_code == 201:
                QMessageBox.information(self, "Success", "쿼리가 성공적으로 저장되었습니다.")
            else:
                QMessageBox.warning(self, "Error", f"쿼리 저장에 실패했습니다: {response.text}")
        except requests.exceptions.RequestException as e:
            QMessageBox.critical(self, "Error", f"오류가 발생했습니다: {str(e)}")


class checkboxItem(QTableWidgetItem):
    def __init__(self):
        super().__init__()
        self.setTextAlignment(Qt.AlignCenter)

    def __lt__(self, other):
        if self.checkState() == other.checkState():
            return super().__lt__(other)
        return self.checkState() == Qt.Checked
