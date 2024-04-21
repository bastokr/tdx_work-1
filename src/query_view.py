from PyQt5.QtWidgets import *  
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QWidget
from PyQt5.QtWidgets import *

from lib.CRUD import CRUD
from widget.addColumn import addColumnWidget
from widget.settingDatabaseWidget import SettingDatabaseWidget
import requests
from PyQt5.QtWidgets import QMessageBox  
 
class QueryView(QWidget):
    def __init__(self):
        super().__init__() 
        self.setupUI()
        self.parameter_widgets = []  # 매개변수 위젯을 저장하는 리스트

    def setupUI(self):
        self.tableWidget = QTableWidget()
        #self.tableWidget.setRowCount(0)
        self.tableWidget.setColumnCount(4)

        self.tableWidget.setEditTriggers(QAbstractItemView.NoEditTriggers)
        # self.tableWidget.setEditTriggers(QAbstractItemView.DoubleClicked)
        # self.tableWidget.setEditTriggers(QAbstractItemView.AllEditTriggers)
        
        self.tableWidget.setHorizontalHeaderLabels(["선택","id", "쿼리id","컬럼명","타입"])  
        #self.tableWidget.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.tableWidget.horizontalHeader().resizeSection(0,50)
        
        #self.tableWidget.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeToContents)

        #for i in range(20):
        #    for j in range(4):
        #        self.tableWidget.setItem(i, j, QTableWidgetItem(str(i+j)))

        layout = QVBoxLayout()
        self.headerLayer = QHBoxLayout();
        
        self.label1 = QLabel("퀄리명:")
        self.textEdit = QLineEdit()
        
        self.btn1 = QPushButton('&컬럼추가', self)
        self.btn1.setCheckable(True)
        self.btn1.toggle()
        self.btn1.setFixedSize(100, 30)  # Set fixed size for the button
        self.btn1.clicked.connect(self.dialog_open)
        
        self.btn2 = QPushButton('&컬럼삭제', self)
        self.btn2.setCheckable(True)
        self.btn2.toggle()
        self.btn2.setFixedSize(100, 30)  # Set fixed size for the button
        self.btn2.clicked.connect(self.delete_row)

        self.btn3 = QPushButton('쿼리 생성', self)
        self.btn3.setCheckable(True)
        self.btn3.toggle()
        self.btn3.setFixedSize(100, 30)  # Set fixed size for the button
        self.btn3.clicked.connect(self.create_query_popup)

        self.headerLayer.addWidget(self.label1)
        
        self.headerLayer.addWidget(self.btn1)
        self.headerLayer.addWidget(self.btn2)
        self.headerLayer.addWidget(self.btn3)

        layout.addLayout(self.headerLayer)
        layout.addWidget(self.tableWidget) 
        
        self.setLayout(layout)

        self.setWindowTitle('QTableWidget')
    
    def message(self,table_id: object, table_nm: str,z:str):
        print(table_id)    
        print(table_nm)  
        self.label1.setText('테이블:'+table_nm)
        print(z) 
        #self.gridinit(table_id, table_nm)
     
 
    def gridinit(self,table_id:object,table_nm:object):
        db = CRUD() 
        self.table_id = table_id;
        self.table_nm = table_nm;
        self.result = db.whereDB( table="tdx_column", colum="*" , where ="table_id='"+str(table_id)+"'")
        i =0
        #result.count
        self.tableWidget.setRowCount(len(self.result))
          
        for i, data in enumerate(self.result):
            item = checkboxItem()

           
             
            item.setFlags(Qt.ItemIsUserCheckable | Qt.ItemIsEnabled)
            item.setCheckState(Qt.CheckState.Unchecked)
            item.setData(Qt.UserRole, item.checkState())
            item.setTextAlignment(Qt.AlignCenter)

            #checklayer.addItem(item)
            #checklayer.setAlignment(Qt.AlignCenter)
            #cellWidget.setLayout(checklayer)

            #item.setTextAlignment( Qt.AlignCenter)


            self.tableWidget.setItem(i, 0, item)
            
            
 
            for j, value in enumerate(data):
                item = QTableWidgetItem(str(value))
                item.setTextAlignment( Qt.AlignCenter)

                self.tableWidget.setItem(i, j+1, item)
            
            self.tableWidget.cellChanged.connect(self.onCellChanged)
                
                
     
    def dialog_open(self):
        self.dialog  = QDialog()
        self.dialog.setWindowTitle('칼럼추가')
        layout = QHBoxLayout(self.dialog ) 
        
        preview = QLabel('', self.dialog )
        addColumn = addColumnWidget(self.table_id,self.table_nm)
        layout.addWidget(addColumn) 
        self.dialog.setWindowModality(Qt.ApplicationModal)
        self.dialog.resize(800, 500)
        addColumn.closeDialog.connect(self.dialog.close)
        addColumn.closeDialog.connect(self.closeRefresh)
        self.dialog.show()

        
    def closeRefresh(self):
        self.gridinit(table_id=self.table_id,table_nm=self.table_nm)

        
    # Dialog 닫기 이벤트
    def dialog_close(self):
        self.dialog.close() 

    # https://freeprog.tistory.com/333 샘플 소스
        
    def onCellChanged(self, row, column):
       
        item = self.tableWidget.item(row, column)
                
        if item is not None:
            row_value = item.row()
            second_item = self.tableWidget.item(row_value, 3)  # Accessing the second item in the same row
            if second_item is not None:
                value_of_second_item = second_item.text()
                print("Value of the second item in the row:", value_of_second_item)
            else:
                print("No second item found in the row:", row_value)

                #print("Row value of the item:", row_value.text(1))
        else:
            print("No item found at row:", row, "and column:", column)

            #print("Row value of the item:", row_value)

        if item is not None:
            if isinstance(item, checkboxItem):  # Assuming checkboxItem is the custom checkbox item class
                state = item.checkState()
                if state == Qt.Checked:
                    print("Checkbox is checked")
                elif state == Qt.Unchecked:
                    print("Checkbox is unchecked")
            else:
                print("Item is not a checkbox")
                 
        else:
            print("No item found at row:", row, "and column:", column)
            

    def delete_row(self):
        #db = CRUD() 
        #db.deleteDB()     
        #self.tableWidget.selectRow
        #db.deleteDB(  table='tdx_column', condition="id != '"++"'")
        selected_row = self.tableWidget.currentRow()
        if selected_row >= 0:
            self.tableWidget.removeRow(selected_row)
        else:
            print("No row selected.")

    def create_query_popup(self):
        self.query_dialog = QDialog(self)
        self.query_dialog.setWindowTitle("Create Query")
        self.query_dialog.setFixedSize(800, 600)
        layout = QVBoxLayout()

        layout.addWidget(QLabel("Name:"))
        self.query_name_input = QLineEdit()
        layout.addWidget(self.query_name_input)

        # SQL Query Editor
        layout.addWidget(QLabel("SQL Query:"))
        self.query_input = QTextEdit()  # 실제 사용 시 향상된 텍스트 에디터로 교체 필요
        self.query_input.setFixedHeight(200)
        layout.addWidget(self.query_input)

        # Parameters Section
        params_container = QWidget()  # 스크롤 영역에 들어갈 컨테이너
        self.params_layout = QVBoxLayout(params_container)
        params_header = QHBoxLayout()  # 헤더 레이아웃에 레이블을 추가
        params_header.addWidget(QLabel("Name"))
        params_header.addWidget(QLabel("Data Type"))
        params_header.addWidget(QLabel("Value"))
        layout.addLayout(params_header)  # 상단에 헤더 레이아웃 추가
        params_scroll_area = QScrollArea()  # 스크롤 영역 생성
        params_scroll_area.setWidgetResizable(True)
        params_scroll_area.setWidget(params_container)
        layout.addWidget(params_scroll_area)

        # Add Parameter Button
        button_layout = QHBoxLayout()
        add_param_btn = QPushButton('Add Parameter')
        add_param_btn.clicked.connect(self.add_parameter)
        button_layout.addWidget(add_param_btn)
        button_layout.addStretch(1)  # 오른쪽 정렬을 위해 스트레치 추가
        layout.addLayout(button_layout)

        # Save Query Button
        save_query_btn = QPushButton('Save Query')
        save_query_btn.clicked.connect(self.save_query)
        layout.addWidget(save_query_btn)

        self.query_dialog.setLayout(layout)
        self.query_dialog.exec_()

    def add_parameter(self):
        param_widget = QWidget()
        param_layout = QHBoxLayout(param_widget)

        # 이름 입력 필드
        name_input = QLineEdit()

        # 데이터 타입 선택 드롭다운
        type_input = QComboBox()
        # 데이터 타입 옵션 추가
        data_types = [
            "smallint", "integer", "bigint", "decimal", "numeric", "real", "double precision", "smallserial",
            "serial", "bigserial", "char(n)", "varchar(n)", "text", "bytea", "timestamp",
            "timestamp with time zone", "date", "time", "time with time zone", "interval", "boolean",
            "enum", "point", "line", "lseg", "box", "path", "polygon", "circle", "cidr", "inet",
            "macaddr", "macaddr8", "bit(n)", "bit varying(n)", "tsvector", "tsquery", "uuid", "xml",
            "json", "jsonb", "int4range", "int8range", "numrange", "tsrange", "daterange"
        ]
        type_input.addItems(data_types)

        # 값 입력 필드
        value_input = QLineEdit()

        # 삭제 버튼
        delete_btn = QPushButton("Delete")
        delete_btn.clicked.connect(lambda: self.remove_parameter(param_widget))

        param_layout.addWidget(name_input)
        param_layout.addWidget(type_input)
        param_layout.addWidget(value_input)
        param_layout.addWidget(delete_btn)

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
            name = name_input.text()
            type_ = type_input.currentText()  # Assuming type_input is a QComboBox
            value = value_input.text()
            parameters.append({"parameter": name, "attribute": type_})

        # Prepare the data dictionary to match the expected JSON structure
        query_data = {
            "title": query_name,
            "query": query_text,
            "parameters": parameters
        }

        # URL to the API endpoint
        url = "http://localhost:8081/api/v1/query"

        try:
            response = requests.post(url, json=query_data)
            if response.status_code == 201:
                QMessageBox.information(self, "Success", "Query saved successfully")
            else:
                QMessageBox.warning(self, "Error", f"Failed to save query: {response.text}")
        except requests.exceptions.RequestException as e:
            QMessageBox.critical(self, "Error", f"An error occurred: {str(e)}")

        self.query_dialog.accept()

class checkboxItem(QTableWidgetItem):
    def __init__(self):
        super().__init__()
        self.setTextAlignment(Qt.AlignCenter)  # Align checkbox to center

    #정렬시 발생 이벤트
    def __lt__(self, other):
        if self.checkState() == other.checkState() or self.checkState() == Qt.Checked:
            return False
        return True

    