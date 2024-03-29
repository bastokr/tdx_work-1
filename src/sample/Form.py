from PyQt5.QtWidgets import *  
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QWidget
from PyQt5.QtWidgets import *

class Form(QWidget):
    """
    만들고자 하는 프로그램의 기본이 되는 창 또는 폼 위젯.
    본 위젯 위에 다른 위젯을 올려서 모양을 만든다.

    QWidget을 상속받아서 필요한 메소드를 작성.
    """

    def __init__(self):
        """
        보통 __init__ (생성자)에서 필요한 것들을 다를 위젯들을 선언해줘도 되지만 init_widget을 따로 만들어서 호출한다.
        """
        QWidget.__init__(self, flags=Qt.Widget)
        self.init_widget()

    def init_widget(self):
        """
        현재 위젯의 모양등을 초기화
        """
        self.setWindowTitle("Hello World")
