from PyQt5.QtWidgets import *  
from PyQt5.QtWidgets import QWidget
from PyQt5.QtWidgets import *


class CustomWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        # Create your custom widget's UI
        label = QLabel('This is a custom widget')
        button = QPushButton('Click Me')

        layout = QVBoxLayout()
        layout.addWidget(label)
        layout.addWidget(button)
        self.setLayout(layout)