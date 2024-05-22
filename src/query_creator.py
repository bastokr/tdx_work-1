from PyQt5.QtWidgets import QApplication, QDialog, QVBoxLayout, QLabel, QLineEdit, QTextEdit, QWidget, QPushButton, QHBoxLayout, QScrollArea, QMessageBox, QComboBox
import requests

from lib.crud import Crud

class QueryCreator(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.parameter_widgets = []
        self.setup_ui()

    def setup_ui(self):
        self.setWindowTitle("Create Query")
        self.setFixedSize(500, 600)
        layout = QVBoxLayout()

        # Parameters Section
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

        # Add Parameter Button
        button_layout = QHBoxLayout()
        add_param_btn = QPushButton('Add Parameter')
        add_param_btn.clicked.connect(lambda: self.add_parameter("", ""))
        button_layout.addWidget(add_param_btn)
        button_layout.addStretch(1)
        layout.addLayout(button_layout)
        
        # Save Query Button
        save_query_btn = QPushButton('Save Query')
        save_query_btn.clicked.connect(self.save_query)
        #layout.addStretch(1) 
        layout.addWidget(save_query_btn)

        self.setLayout(layout)
    
    def default_param(self,id):
        self.parameter_widgets = []
        db = Crud()
        self.id = id; 
        self.result = db.whereDB( table="tdx_query_param", column="*" , where ="tdx_query_id='"+str(id)+"'")
        i =0
        #result.count
           
        for i, data in enumerate(self.result):
            self.add_parameter(data[2], data[1])

                 

    def add_parameter(self,colname,datatype):
        param_widget = QWidget()
        param_widget.setStyleSheet("color: white; padding: 4px 4px 4px 4px; border: none; border-radius: 1px;")  # Remove border
         
        param_layout = QHBoxLayout(param_widget)
        name_input = QLineEdit()
        type_input = QComboBox()
        data_types = [
            "smallint", "integer", "bigint", "decimal", "numeric", "real", "double precision", "smallserial",
            "serial", "bigserial", "char(n)", "varchar(n)", "text", "bytea", "timestamp",
            "timestamp with time zone", "date", "time", "time with time zone", "interval", "boolean",
            "enum", "point", "line", "lseg", "box", "path", "polygon", "circle", "cidr", "inet",
            "macaddr", "macaddr8", "bit(n)", "bit varying(n)", "tsvector", "tsquery", "uuid", "xml",
            "json", "jsonb", "int4range", "int8range", "numrange", "tsrange", "daterange"
        ]
        type_input.addItems(data_types)
        value_input = QLineEdit()
        delete_btn = QPushButton("Delete")
        delete_btn.setStyleSheet("background-color: #4CAF50; color: white; padding: 5px 5px; border: none; border-radius: 2px; margin: 0px;")
    
        delete_btn.clicked.connect(lambda: self.remove_parameter(param_widget))
        param_layout.addWidget(name_input)
        param_layout.addWidget(type_input)
        param_layout.addWidget(value_input)
        param_layout.addWidget(delete_btn)
        
        name_input.setText(colname)
        type_input.setCurrentText(datatype)
        
        self.params_layout.addWidget(param_widget)
        self.params_layout.insertWidget(self.params_layout.count()-2,param_widget)
        if(self.params_layout.count()==1):
            self.params_layout.addStretch(1) 
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
                QMessageBox.information(self, "Success", "Query saved successfully")
            else:
                QMessageBox.warning(self, "Error", f"Failed to save query: {response.text}")
        except requests.exceptions.RequestException as e:
            QMessageBox.critical(self, "Error", f"An error occurred: {str(e)}")

    def loadQuery(self, query):
        try:
            self.query_name_input.setText(query.get('title', ''))
            self.query_input.setText(query.get('query', ''))
            for param in query.get('parameters', []):
                self.add_parameter()
                widget_tuple = self.parameter_widgets[-1]
                widget_tuple[1].setText(param.get('parameter', ''))
                widget_tuple[2].setCurrentText(param.get('attribute', ''))
                widget_tuple[3].setText(param.get('value', ''))
        except Exception as e:
            QMessageBox.critical(self, "Error Loading Query", f"Failed to load query details: {str(e)}")


if __name__ == "__main__":
    import sys
    app = QApplication(sys.argv)
    editor = QueryCreator()
    editor.exec_()
