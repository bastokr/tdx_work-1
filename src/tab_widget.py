from PyQt5.QtWidgets import QWidget, QTabWidget, QVBoxLayout

class TabWidget(QWidget):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout()
        self.tab_widget = QTabWidget()
        
        console_tab = QWidget()
        terminal_tab = QWidget()
        
        self.tab_widget.addTab(console_tab, "Console")
        self.tab_widget.addTab(terminal_tab, "Terminal")
        
        layout.addWidget(self.tab_widget)
        self.setLayout(layout)
    
    def addTab(self, widget, title):
        self.tab_widget.addTab(widget, title)