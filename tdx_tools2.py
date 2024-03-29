import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QSplitter, QTextEdit, QLabel
from PyQt5.QtCore import Qt  # Import the Qt namespace from QtCore

class MyWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Layered Application")
        self.setGeometry(200, 200, 800, 600)

        splitter = QSplitter(Qt.Horizontal)  # Use Qt namespace from QtCore

        # Add widgets to the splitter's areas
        left_widget = QTextEdit()
        right_widget = QLabel("Layer 2")
        splitter.addWidget(left_widget)
        splitter.addWidget(left_widget)
        splitter.addWidget(right_widget)

        self.setCentralWidget(splitter)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MyWindow()
    window.show()
    sys.exit(app.exec_())