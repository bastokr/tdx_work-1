from PyQt5.QtWidgets import *  
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QWidget
from PyQt5.QtWidgets import *

from lib.CRUD import CRUD
from widget.addColumn import addColumnWidget
from widget.settingDatabaseWidget import SettingDatabaseWidget
import requests
from PyQt5.QtWidgets import QMessageBox
from QueryCreator import QueryCreator

class MainList(QWidget):
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
        
        self.tableWidget.setHorizontalHeaderLabels(["선택","id", "테이브id","컬럼명","타입"])  
        #self.tableWidget.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.tableWidget.horizontalHeader().resizeSection(0,50)
        
        #self.tableWidget.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeToContents)

        #for i in range(20):
        #    for j in range(4):
        #        self.tableWidget.setItem(i, j, QTableWidgetItem(str(i+j)))

        layout = QVBoxLayout()
        self.headerLayer = QHBoxLayout();
        
        self.label1 = QLabel("테이블명:")
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
        self.gridinit(table_id, table_nm)
     
 
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
        dialog = QueryCreator(self)
        dialog.show()

class checkboxItem(QTableWidgetItem):
    def __init__(self):
        super().__init__()
        self.setTextAlignment(Qt.AlignCenter)  # Align checkbox to center

    #정렬시 발생 이벤트
    def __lt__(self, other):
        if self.checkState() == other.checkState() or self.checkState() == Qt.Checked:
            return False
        return True

    