from PyQt5.QtWidgets import QWidget, QTabWidget, QVBoxLayout, QSplitter, QPushButton, QStyleFactory
from PyQt5.QtGui import QIcon, QFont

class TabWidget(QWidget):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout()
        self.splitter = QSplitter()
        self.tab_widget = QTabWidget()
        
        console_tab = QWidget()
        terminal_tab = QWidget()
        
        self.tab_widget.addTab(console_tab, "Console")
        self.tab_widget.addTab(terminal_tab, "Terminal")
        
        self.splitter.addWidget(self.tab_widget)
        layout.addWidget(self.splitter)
        
        self.toggle_button = QPushButton()
        self.toggle_button.setIcon(QIcon('src/img/toggle.png'))
        self.toggle_button.setStyleSheet("""
            QPushButton {
                background-color: #4CAF50;  # Green background
                color: #ffffff;  # White text
                border: 1px solid #ccc;
                padding: 10px 20px;  # Adjusted padding
                border-radius: 5px;
                margin: 0px;  # Remove margin
                font-family: 'Helvetica Neue', Helvetica, Arial, sans-serif;  # Updated font
                font-size: 16px;  # Larger font size
                font-weight: bold;  # Bold text
            }
            QPushButton:hover {
                background-color: #45a049;  # Darker green on hover
            }
        """)
        self.toggle_button.clicked.connect(self.toggleVisibility)
        layout.addWidget(self.toggle_button)
        
        self.setLayout(layout)
    
    def toggleVisibility(self):
        if self.tab_widget.isVisible():
            self.tab_widget.hide()
        else:
            self.tab_widget.show()

