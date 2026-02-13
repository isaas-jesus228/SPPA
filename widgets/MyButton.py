from PyQt6.QtWidgets import QPushButton, QToolTip
from PyQt6.QtCore import QPoint

class MyButton(QPushButton):
    def __init__(self, text):
        super().__init__(text)
        self.tt = ""

    def mousePressEvent(self, e):
        QToolTip.showText(self.mapToGlobal(QPoint(0, self.height())), self.tt, self)
        super().mousePressEvent(e)

    def set_tt(self, text):
        self.tt = text