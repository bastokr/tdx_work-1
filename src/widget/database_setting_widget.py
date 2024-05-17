
import sys
from PyQt5.QtWidgets import QDialog, QVBoxLayout, QLabel, QLineEdit, QPushButton, QHBoxLayout, QMessageBox
from PyQt5.QtCore import pyqtSignal
from lib.crud import Crud

class DatabaseSettingWidget(QDialog):
    closeDialog = pyqtSignal(dict)  # type: ignore

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupUI()

    def setupUI(self):
        self.setWindowTitle("Database Settings")

        layout = QVBoxLayout()

        # 기본값 설정
        default_host = "211.232.75.41"
        default_dbname = "tdx_db"
        default_user = "tdx_user"
        default_password = "tdx_password"
        default_port = "5433"

        # Host
        self.host_label = QLabel("Host:")
        self.host_input = QLineEdit()
        self.host_input.setText(default_host)
        layout.addWidget(self.host_label)
        layout.addWidget(self.host_input)

        # Database
        self.db_label = QLabel("Database Name:")
        self.db_input = QLineEdit()
        self.db_input.setText(default_dbname)
        layout.addWidget(self.db_label)
        layout.addWidget(self.db_input)

        # User
        self.user_label = QLabel("User:")
        self.user_input = QLineEdit()
        self.user_input.setText(default_user)
        layout.addWidget(self.user_label)
        layout.addWidget(self.user_input)

        # Password
        self.password_label = QLabel("Password:")
        self.password_input = QLineEdit()
        self.password_input.setEchoMode(QLineEdit.Password)
        self.password_input.setText(default_password)
        layout.addWidget(self.password_label)
        layout.addWidget(self.password_input)

        # Port
        self.port_label = QLabel("Port:")
        self.port_input = QLineEdit()
        self.port_input.setText(default_port)
        layout.addWidget(self.port_label)
        layout.addWidget(self.port_input)

        # Buttons
        button_layout = QHBoxLayout()
        self.save_button = QPushButton("Save")
        self.save_button.clicked.connect(self.save_settings)
        self.close_button = QPushButton("Close")
        self.close_button.clicked.connect(self.close)
        button_layout.addWidget(self.save_button)
        button_layout.addWidget(self.close_button)

        layout.addLayout(button_layout)
        self.setLayout(layout)

    def save_settings(self):
        settings = {
            "host": self.host_input.text(),
            "dbname": self.db_input.text(),
            "user": self.user_input.text(),
            "password": self.password_input.text(),
            "port": self.port_input.text(),
        }

        # 데이터베이스 연결 테스트
        db = Crud()
        if db.test_connection(settings):
            # 연결 성공
            self.closeDialog.emit(settings)
            self.close()
        else:
            # 연결 실패
            QMessageBox.critical(self, "Connection Failed", "Failed to connect to the database with the provided settings.")