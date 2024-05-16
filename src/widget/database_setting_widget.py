# src/widget/database_setting_widget.py

import sys
from PyQt5.QtWidgets import QDialog, QVBoxLayout, QLabel, QLineEdit, QPushButton, QHBoxLayout, QMessageBox
from PyQt5.QtCore import pyqtSignal

class DatabaseSettingWidget(QDialog):
    closeDialog = pyqtSignal(dict) # type: ignore

    def __init__(self):
        super().__init__()

        self.setupUI()

    def setupUI(self):
        self.setWindowTitle("Database Settings")

        layout = QVBoxLayout()

        # Host
        self.host_label = QLabel("Host:")
        self.host_input = QLineEdit()
        layout.addWidget(self.host_label)
        layout.addWidget(self.host_input)

        # Database
        self.db_label = QLabel("Database Name:")
        self.db_input = QLineEdit()
        layout.addWidget(self.db_label)
        layout.addWidget(self.db_input)

        # User
        self.user_label = QLabel("User:")
        self.user_input = QLineEdit()
        layout.addWidget(self.user_label)
        layout.addWidget(self.user_input)

        # Password
        self.password_label = QLabel("Password:")
        self.password_input = QLineEdit()
        self.password_input.setEchoMode(QLineEdit.Password)
        layout.addWidget(self.password_label)
        layout.addWidget(self.password_input)

        # Port
        self.port_label = QLabel("Port:")
        self.port_input = QLineEdit()
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

        # Emit signal with settings
        self.closeDialog.emit(settings)
        self.close()
