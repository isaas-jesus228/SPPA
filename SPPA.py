from windows.Settings import *
from sys import argv, exit
from PyQt6.QtWidgets import QApplication

app = QApplication(argv)

wSettings = WinSettings()

exit(app.exec())