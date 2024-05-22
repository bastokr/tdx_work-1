import sys
import configparser
from PyQt5.QtWidgets import QDialog, QVBoxLayout, QLabel, QLineEdit, QPushButton, QHBoxLayout, QMessageBox
from PyQt5.QtCore import pyqtSignal

# 현재 파일의 디렉토리 경로를 추가합니다.
import os
current_directory = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.join(current_directory, '..'))

from lib.crud import Crud

CONFIG_FILE = os.path.join(current_directory, '..', 'config.ini')


class DatabaseSettingWidget(QDialog):
    closeDialog = pyqtSignal(dict)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.config = configparser.ConfigParser()
        self.load_config()
        self.setupUI()

    def load_config(self):
        self.config.read(CONFIG_FILE)
        if not self.config.has_section('Database'):
            self.config.add_section('Database')
            return
        self.host = self.config.get('Database', 'host', fallback='')
        self.dbname = self.config.get('Database', 'dbname', fallback='')
        self.user = self.config.get('Database', 'user', fallback='')
        self.password = self.config.get('Database', 'password', fallback='')
        self.port = self.config.get('Database', 'port', fallback='')

    def setupUI(self):
        self.setWindowTitle("Database Settings")

        layout = QVBoxLayout()

        # Host
        self.host_label = QLabel("Host:")
        self.host_input = QLineEdit()
        self.host_input.setText(self.host)
        layout.addWidget(self.host_label)
        layout.addWidget(self.host_input)

        # Database
        self.db_label = QLabel("Database Name:")
        self.db_input = QLineEdit()
        self.db_input.setText(self.dbname)
        layout.addWidget(self.db_label)
        layout.addWidget(self.db_input)

        # User
        self.user_label = QLabel("User:")
        self.user_input = QLineEdit()
        self.user_input.setText(self.user)
        layout.addWidget(self.user_label)
        layout.addWidget(self.user_input)

        # Password
        self.password_label = QLabel("Password:")
        self.password_input = QLineEdit()
        self.password_input.setEchoMode(QLineEdit.Password)
        self.password_input.setText(self.password)
        layout.addWidget(self.password_label)
        layout.addWidget(self.password_input)

        # Port
        self.port_label = QLabel("Port:")
        self.port_input = QLineEdit()
        self.port_input.setText(self.port)
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
        self.config.set('Database', 'host', self.host_input.text())
        self.config.set('Database', 'dbname', self.db_input.text())
        self.config.set('Database', 'user', self.user_input.text())
        self.config.set('Database', 'password', self.password_input.text())
        self.config.set('Database', 'port', self.port_input.text())

        with open(CONFIG_FILE, 'w') as configfile:
            self.config.write(configfile)

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

if __name__ == "__main__":
    from PyQt5.QtWidgets import QApplication
    app = QApplication(sys.argv)
    widget = DatabaseSettingWidget()
    widget.show()
    sys.exit(app.exec_())
