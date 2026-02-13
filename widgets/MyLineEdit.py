from PyQt6 import QtWidgets

class MyLineEdit(QtWidgets.QLineEdit):
    def __init__(self):
        super().__init__()
        self.id = None
    
    def setId(self, text):
        self.id = text

    def getId(self):
        return self.id