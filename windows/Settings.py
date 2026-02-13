from PyQt6 import QtWidgets
from PyQt6.QtWidgets import QMainWindow, QWidget, QFileDialog
from PyQt6.QtGui import QIcon
from windows.PaintGraphics import *
from functions.Functions import *
from widgets.MyLineEdit import *
from widgets.MyButton import *
from MyLib.ML import *
from math import degrees, asin, sqrt

class WinSettings(QMainWindow):

    def __init__(self):
        super().__init__()

        #Поля
        self.monitor = get_monitor()
        self.WIDTH = 240
        self.HEIGHT = 380
        self.x = self.monitor.width//3 - self.WIDTH//3
        self.y = self.monitor.height//3 - self.HEIGHT//3
        self.func = None
        self.child = 0
        self.myLayout = QtWidgets.QVBoxLayout() 
        self.is_noting = True

        self.Initialization()   

        #КомбоБокс - сигналы
        self.func_variants.currentTextChanged.connect(self.changed)

        self.show()

    #Инициализация виджетов
    def Initialization(self):
        self.setWindowTitle("Настройки")
        self.setWindowIcon(QIcon("icon.ico"))
        self.setGeometry(self.x, self.y, self.WIDTH, self.HEIGHT)
        self.setFixedSize(self.WIDTH, self.HEIGHT)

        self.func_variants = QtWidgets.QComboBox()
        self.func_variants.move(self.WIDTH//2 - self.func_variants.width()//2, 0)
        self.func_variants.addItems(["Функции", "Окружность", "Спираль Архимеда", "Полярная Роза", "Улитка Паскаля", "Локон Аньези", "Декартов Лист", "Астроида", "Полярная Астроида", "Эпициклоида", "Гипоциклоида"])
        self.myLayout.addWidget(self.func_variants, alignment=Qt.AlignmentFlag.AlignTop)

        widget = QWidget()
        widget.setLayout(self.myLayout)
        self.setCentralWidget(widget)

        self.create_settings_func()

    #При смене значения ComboBox
    def changed(self, text):
        match text:
            case "Функции":
                self.func = None
                self.delete_widgets()

                self.create_settings_func()

                self.is_noting = True

                self.close_graphic()

            case "Окружность":
                self.delete_widgets()

                self.is_noting = False

                self.close_graphic()

                self.func = None
                self.func = Circle()
                self.create_settings_circle()
                self.update_values()
                
                self.child = WinPaintGraphics(self, self.func, "polar", "norm")

            case "Полярная Роза":
                self.delete_widgets()

                self.is_noting = False

                self.close_graphic()

                self.func = None
                self.func = PolarRose()
                self.create_settings_polar_rose()
                self.update_values()

                self.child = WinPaintGraphics(self, self.func, "polar", "pr")

            case "Улитка Паскаля":
                self.delete_widgets()

                self.is_noting = False

                self.close_graphic()

                self.func = None
                self.func = SnailPascal()
                self.create_settings_snail_pascal()
                self.update_values()

                self.child = WinPaintGraphics(self, self.func, "param", "norm")

            case "Декартов Лист":
                self.delete_widgets()

                self.is_noting = False

                self.close_graphic()

                self.func = None
                self.create_settings_dekart()
                self.func = Dekart()
                self.update_values()

                self.child = WinPaintGraphics(self, self.func, "param", "nc")

            case "Спираль Архимеда":
                self.delete_widgets()

                self.is_noting = False

                self.close_graphic()

                self.func = None
                self.create_settings_spiral()
                self.func = Spiral()
                self.update_values()

                self.child = WinPaintGraphics(self, self.func, "polar", "sp")

            case "Локон Аньези":
                self.delete_widgets()

                self.is_noting = False

                self.close_graphic()

                self.func = None
                self.create_settings_anyez()
                self.func = Anyez()
                self.update_values()

                self.child = WinPaintGraphics(self, self.func, "param", "sp")
            
            case "Полярная Астроида":
                self.delete_widgets()

                self.is_noting = False

                self.close_graphic()

                self.func = None
                self.func = PolarAstroid()
                self.create_settings_polar_astroid()
                self.update_values()
                
                self.child = WinPaintGraphics(self, self.func, "polar", "nncc")

            case "Астроида":
                self.delete_widgets()

                self.is_noting = False

                self.close_graphic()

                self.func = None
                self.func = Astroid()
                self.create_settings_astroid()
                self.update_values()
                
                self.child = WinPaintGraphics(self, self.func, "param", "norm")

            case "Эпициклоида":
                self.delete_widgets()

                self.is_noting = False

                self.close_graphic()

                self.func = None
                self.func = Epicycloid()
                self.create_settings_epicycloid()
                self.update_values()
                
                self.child = WinPaintGraphics(self, self.func, "param", "ep")

            case "Гипоциклоида":
                self.delete_widgets()

                self.is_noting = False

                self.close_graphic()

                self.func = None
                self.func = Hypocycloid()
                self.create_settings_hypocycloid()
                self.update_values()
                
                self.child = WinPaintGraphics(self, self.func, "param", "ep")

    #Удаление виджетов
    def delete_widgets(self):
        #Удаление пружины
        if not self.is_noting:
            self.myLayout.removeItem(self.myLayout.itemAt(self.myLayout.count()-1))

        #Удаление лишних виджетов
        for i in reversed(range(0, self.myLayout.count())):
            item = self.myLayout.itemAt(i)
            widget = item.widget()
            if widget.__class__.__name__ != "QComboBox" and widget is not None:
                self.myLayout.removeWidget(widget)
                widget.deleteLater()

    #Ивент закрытия главного окна
    def closeEvent(self, event):
        if hasattr(self, "child") and self.child != 0:
            self.child.view.close()
        event.accept()

    def show_saved_win(self):
        file_name, _ = QFileDialog.getSaveFileName(self, 'Save File', './saves', 'Text Files (*.txt)')

        if file_name:
            with open(file_name, 'w', encoding="utf-8") as file:
                match self.child.ws:
                    case "polar":
                        self.table_polar(file)
                    case "param":
                        self.table_param(file)

    #Параметры для грфиков
    def create_settings_func(self):
        txt = shenter_text("Приветствую вас в программе SPPA!!!\nОна строит заранее предустановленные графики в полярной системе координат или параметрически заданные. Данная программа поможет исследовать зависимость вида графика от параметров функции. Ещё вы сможете сохранить таблицу значений выбранной функции.\n\nПредупреждение!!!\nПри выставлении большой точности программа будет зависать из-за большого кол-ва значений и в некоторых случаях при выставлении слишком больших или маленьких значений параметров.", 27)
        self.text = QtWidgets.QLabel(txt)

        self.myLayout.addWidget(self.text, alignment=Qt.AlignmentFlag.AlignTop)

    def create_settings_circle(self):
        info = "<b>Окружность</b> - это геометрическое место точек плоскости, расстояние от каждой из которых до данной точки, называемой центром, есть величина постоянная.<br><br>a - радиус окружности."

        #Параметры
        self.text1 = QtWidgets.QLabel("Параметр a:")
        self.le1 = MyLineEdit()
        self.text2 = QtWidgets.QLabel("Точность:")
        self.accuracy = MyLineEdit()
        self.cbab = QtWidgets.QCheckBox("Градусный график")
        self.button_save = QtWidgets.QPushButton("Сохранить как...")
        self.button_info = MyButton("i")

        self.button_info.set_tt(shenter_text(info))
        self.button_info.setFixedSize(22, 22)

        self.le1.setId("param")
        self.accuracy.setId("acc")

        self.le1.setText("10")
        self.accuracy.setText("1")

        #Дабваление в сетку
        self.myLayout.addWidget(self.text1, alignment=Qt.AlignmentFlag.AlignTop)
        self.myLayout.addWidget(self.le1, alignment=Qt.AlignmentFlag.AlignTop)
        self.myLayout.addWidget(self.text2, alignment=Qt.AlignmentFlag.AlignTop)
        self.myLayout.addWidget(self.accuracy, alignment=Qt.AlignmentFlag.AlignTop)
        self.myLayout.addWidget(self.cbab, alignment=Qt.AlignmentFlag.AlignTop)
        self.myLayout.addWidget(self.button_save, alignment=Qt.AlignmentFlag.AlignTop)
        self.myLayout.addWidget(self.button_info, alignment=Qt.AlignmentFlag.AlignTop)

        self.myLayout.addWidget(self.button_info, alignment=Qt.AlignmentFlag.AlignHCenter)

        self.le1.textChanged.connect(self.update_paint)
        self.accuracy.textChanged.connect(self.update_paint)
        self.cbab.stateChanged.connect(self.update_paint)
        self.button_save.clicked.connect(self.show_saved_win)

        #Пружина
        self.myLayout.addStretch()

    def create_settings_polar_rose(self):
        info = "<b>Полярная Роза</b> — плоская кривая, напоминающая символическое изображение цветка.<br><br>a - множитель размера розы<br>b - кол-во лепестков (чётное кол-во увеличивается в два раза)"

        #Параметры
        self.text1 = QtWidgets.QLabel("Параметр a:")
        self.le1 = MyLineEdit()
        self.text2 = QtWidgets.QLabel("Параметр b:")
        self.le2 = MyLineEdit()
        self.text3 = QtWidgets.QLabel("Точность:")
        self.accuracy = MyLineEdit()
        self.cbab = QtWidgets.QCheckBox("Градусный график")
        self.button_save = QtWidgets.QPushButton("Сохранить как...")
        self.button_info = MyButton("i")

        self.button_info.set_tt(shenter_text(info))
        self.button_info.setFixedSize(22, 22)

        self.le1.setId("param")
        self.le2.setId("param")
        self.accuracy.setId("acc")

        self.le1.setText("10")
        self.le2.setText("1")
        self.accuracy.setText("1")

        #Дабваление в сетку
        self.myLayout.addWidget(self.text1, alignment=Qt.AlignmentFlag.AlignTop)
        self.myLayout.addWidget(self.le1, alignment=Qt.AlignmentFlag.AlignTop)
        self.myLayout.addWidget(self.text2, alignment=Qt.AlignmentFlag.AlignTop)
        self.myLayout.addWidget(self.le2, alignment=Qt.AlignmentFlag.AlignTop)
        self.myLayout.addWidget(self.text3, alignment=Qt.AlignmentFlag.AlignTop)
        self.myLayout.addWidget(self.accuracy, alignment=Qt.AlignmentFlag.AlignTop)
        self.myLayout.addWidget(self.cbab, alignment=Qt.AlignmentFlag.AlignTop)
        self.myLayout.addWidget(self.button_save, alignment=Qt.AlignmentFlag.AlignTop)
        self.myLayout.addWidget(self.button_info, alignment=Qt.AlignmentFlag.AlignTop)

        self.myLayout.addWidget(self.button_info, alignment=Qt.AlignmentFlag.AlignHCenter)

        self.le1.textChanged.connect(self.update_paint)
        self.le2.textChanged.connect(self.update_paint)
        self.accuracy.textChanged.connect(self.update_paint)
        self.cbab.stateChanged.connect(self.update_paint)
        self.button_save.clicked.connect(self.show_saved_win)

        #Пружина
        self.myLayout.addStretch()

    def create_settings_snail_pascal(self):
        info = "<b>Улитка Паскаля</b> - это конхоида (особая кривая) окружности с полюсом на этой окружности."
        
        #Параметры
        self.text1 = QtWidgets.QLabel("Параметр a:")
        self.le1 = MyLineEdit()
        self.text2 = QtWidgets.QLabel("Параметр b:")
        self.le2 = MyLineEdit()
        self.text3 = QtWidgets.QLabel("Точность:")
        self.accuracy = MyLineEdit()
        self.button_save = QtWidgets.QPushButton("Сохранить как...")
        self.button_info = MyButton("i")

        self.button_info.set_tt(shenter_text(info))
        self.button_info.setFixedSize(22, 22)

        self.le1.setId("param")
        self.le2.setId("param")
        self.accuracy.setId("acc")

        self.le1.setText("1")
        self.le2.setText("1")
        self.accuracy.setText("1")

        #Дабваление в сетку
        self.myLayout.addWidget(self.text1, alignment=Qt.AlignmentFlag.AlignTop)
        self.myLayout.addWidget(self.le1, alignment=Qt.AlignmentFlag.AlignTop)
        self.myLayout.addWidget(self.text2, alignment=Qt.AlignmentFlag.AlignTop)
        self.myLayout.addWidget(self.le2, alignment=Qt.AlignmentFlag.AlignTop)
        self.myLayout.addWidget(self.text3, alignment=Qt.AlignmentFlag.AlignTop)
        self.myLayout.addWidget(self.accuracy, alignment=Qt.AlignmentFlag.AlignTop)
        self.myLayout.addWidget(self.button_save, alignment=Qt.AlignmentFlag.AlignTop)
        self.myLayout.addWidget(self.button_info, alignment=Qt.AlignmentFlag.AlignTop)

        self.myLayout.addWidget(self.button_info, alignment=Qt.AlignmentFlag.AlignHCenter)

        self.le1.textChanged.connect(self.update_paint)
        self.le2.textChanged.connect(self.update_paint)
        self.accuracy.textChanged.connect(self.update_paint)
        self.button_save.clicked.connect(self.show_saved_win)

        #Пружина
        self.myLayout.addStretch()

    def create_settings_dekart(self):
        info = "<b>Декартов лист</b> - линия, которая состоит из петли и двух бесконечных ветвей.<br><br>a - множитель увеличения листа"
        
        #Параметры
        self.text1 = QtWidgets.QLabel("Параметр a:")
        self.le1 = MyLineEdit()
        self.text2 = QtWidgets.QLabel("Точность:")
        self.accuracy = MyLineEdit()
        self.button_save = QtWidgets.QPushButton("Сохранить как...")
        self.button_info = MyButton("i")

        self.button_info.set_tt(shenter_text(info))
        self.button_info.setFixedSize(22, 22)

        self.le1.setId("param")
        self.accuracy.setId("acc")

        self.le1.setText("1")
        self.accuracy.setText("1")

        #Дабваление в сетку
        self.myLayout.addWidget(self.text1, alignment=Qt.AlignmentFlag.AlignTop)
        self.myLayout.addWidget(self.le1, alignment=Qt.AlignmentFlag.AlignTop)
        self.myLayout.addWidget(self.text2, alignment=Qt.AlignmentFlag.AlignTop)
        self.myLayout.addWidget(self.accuracy, alignment=Qt.AlignmentFlag.AlignTop)
        self.myLayout.addWidget(self.button_save, alignment=Qt.AlignmentFlag.AlignTop)
        self.myLayout.addWidget(self.button_info, alignment=Qt.AlignmentFlag.AlignTop)

        self.myLayout.addWidget(self.button_info, alignment=Qt.AlignmentFlag.AlignHCenter)

        self.le1.textChanged.connect(self.update_paint)
        self.accuracy.textChanged.connect(self.update_paint)
        self.button_save.clicked.connect(self.show_saved_win)

        #Пружина
        self.myLayout.addStretch()

    def create_settings_spiral(self):
        info = "<b>Спираль Архимеда</b> — это плоская кривая, которая образуется путём равномерного увеличения радиуса при вращении точки вокруг центра.<br><br>a - множитель для итогвого радиуса<br>b - слагаемое для итогового радиуса"

        #Параметры
        self.text1 = QtWidgets.QLabel("Параметр a:")
        self.le1 = MyLineEdit()
        self.text2 = QtWidgets.QLabel("Параметр b:")
        self.le2 = MyLineEdit()
        self.text3 = QtWidgets.QLabel("От:")
        self.le3 = MyLineEdit()
        self.text4 = QtWidgets.QLabel("До:")
        self.le4 = MyLineEdit()
        self.text5 = QtWidgets.QLabel("Точность:")
        self.accuracy = MyLineEdit()
        self.cbab = QtWidgets.QCheckBox("Градусный график")
        self.button_save = QtWidgets.QPushButton("Сохранить как...")
        self.button_info = MyButton("i")

        self.button_info.set_tt(shenter_text(info))
        self.button_info.setFixedSize(22, 22)

        self.le1.setId("param")
        self.le2.setId("param")
        self.accuracy.setId("acc")

        self.le1.setText("1")
        self.le2.setText("1")
        self.accuracy.setText("1")
        self.le3.setText("-57")
        self.le4.setText("360")

        #Дабваление в сетку
        self.myLayout.addWidget(self.text1, alignment=Qt.AlignmentFlag.AlignTop)
        self.myLayout.addWidget(self.le1, alignment=Qt.AlignmentFlag.AlignTop)
        self.myLayout.addWidget(self.text2, alignment=Qt.AlignmentFlag.AlignTop)
        self.myLayout.addWidget(self.le2, alignment=Qt.AlignmentFlag.AlignTop)
        self.myLayout.addWidget(self.text3, alignment=Qt.AlignmentFlag.AlignTop)
        self.myLayout.addWidget(self.le3, alignment=Qt.AlignmentFlag.AlignTop)
        self.myLayout.addWidget(self.text4, alignment=Qt.AlignmentFlag.AlignTop)
        self.myLayout.addWidget(self.le4, alignment=Qt.AlignmentFlag.AlignTop)
        self.myLayout.addWidget(self.text5, alignment=Qt.AlignmentFlag.AlignTop)
        self.myLayout.addWidget(self.accuracy, alignment=Qt.AlignmentFlag.AlignTop)
        self.myLayout.addWidget(self.cbab, alignment=Qt.AlignmentFlag.AlignTop)
        self.myLayout.addWidget(self.button_save, alignment=Qt.AlignmentFlag.AlignTop)
        self.myLayout.addWidget(self.button_info, alignment=Qt.AlignmentFlag.AlignTop)

        self.myLayout.addWidget(self.button_info, alignment=Qt.AlignmentFlag.AlignHCenter)

        self.le1.textChanged.connect(self.update_paint)
        self.le2.textChanged.connect(self.update_paint)
        self.le3.textChanged.connect(self.update_paint)
        self.le4.textChanged.connect(self.update_paint) 
        self.accuracy.textChanged.connect(self.update_paint)
        self.cbab.stateChanged.connect(self.update_paint)
        self.button_save.clicked.connect(self.show_saved_win)

        #Пружина
        self.myLayout.addStretch()

    def create_settings_anyez(self):
        info = "<b>Локон Аньези</b> - это кривая, которую можно описать как разрез достаточно плотной ткани, лежащей на шаре некого радиуса.<br><br>a - кубическое растяжение графика вдоль оси OY<br>b - кубическое растяжение графика вдоль оси OX"

        #Параметры
        self.text1 = QtWidgets.QLabel("Параметр a:")
        self.le1 = MyLineEdit()
        self.text2 = QtWidgets.QLabel("Параметр b:")
        self.le2 = MyLineEdit()
        self.text3 = QtWidgets.QLabel("От:")
        self.le3 = MyLineEdit()
        self.text4 = QtWidgets.QLabel("До:")
        self.le4 = MyLineEdit()
        self.text5 = QtWidgets.QLabel("Точность:")
        self.accuracy = MyLineEdit()
        self.button_save = QtWidgets.QPushButton("Сохранить как...")
        self.button_info = MyButton("i")

        self.button_info.set_tt(shenter_text(info))
        self.button_info.setFixedSize(22, 22)

        self.le1.setId("param")
        self.le2.setId("param")
        self.accuracy.setId("acc")

        self.le1.setText("1")
        self.le2.setText("1")
        self.accuracy.setText("10")
        self.le3.setText("-100")
        self.le4.setText("100")

        #Дабваление в сетку
        self.myLayout.addWidget(self.text1, alignment=Qt.AlignmentFlag.AlignTop)
        self.myLayout.addWidget(self.le1, alignment=Qt.AlignmentFlag.AlignTop)
        self.myLayout.addWidget(self.text2, alignment=Qt.AlignmentFlag.AlignTop)
        self.myLayout.addWidget(self.le2, alignment=Qt.AlignmentFlag.AlignTop)
        self.myLayout.addWidget(self.text3, alignment=Qt.AlignmentFlag.AlignTop)
        self.myLayout.addWidget(self.le3, alignment=Qt.AlignmentFlag.AlignTop)
        self.myLayout.addWidget(self.text4, alignment=Qt.AlignmentFlag.AlignTop)
        self.myLayout.addWidget(self.le4, alignment=Qt.AlignmentFlag.AlignTop)
        self.myLayout.addWidget(self.text5, alignment=Qt.AlignmentFlag.AlignTop)
        self.myLayout.addWidget(self.accuracy, alignment=Qt.AlignmentFlag.AlignTop)
        self.myLayout.addWidget(self.button_save, alignment=Qt.AlignmentFlag.AlignTop)
        self.myLayout.addWidget(self.button_info, alignment=Qt.AlignmentFlag.AlignTop)

        self.myLayout.addWidget(self.button_info, alignment=Qt.AlignmentFlag.AlignHCenter)

        self.le1.textChanged.connect(self.update_paint)
        self.le2.textChanged.connect(self.update_paint)
        self.le3.textChanged.connect(self.update_paint)
        self.le4.textChanged.connect(self.update_paint)
        self.accuracy.textChanged.connect(self.update_paint)
        self.button_save.clicked.connect(self.show_saved_win)

        #Пружина
        self.myLayout.addStretch()

    def create_settings_polar_astroid(self):
        info = "<b>Полярная Астроида</b> - это баг. Используется функция описывающая Астроиду в полярной системе координат, но почему-то она выглядит иначе.<br><br>a - множитель увеличение горизонтальных 'лепестков'<br>b - множитель увеличение вертикальных 'лепестков'"

        #Параметры
        self.text1 = QtWidgets.QLabel("Параметр a:")
        self.le1 = MyLineEdit()
        self.text2 = QtWidgets.QLabel("Параметр b:")
        self.le2 = MyLineEdit()
        self.text3 = QtWidgets.QLabel("Точность:")
        self.accuracy = MyLineEdit()
        self.cbab = QtWidgets.QCheckBox("Градусный график")
        self.button_save = QtWidgets.QPushButton("Сохранить как...")
        self.button_info = MyButton("i")

        self.button_info.set_tt(shenter_text(info))
        self.button_info.setFixedSize(22, 22)

        self.le1.setId("param")
        self.le2.setId("param")
        self.accuracy.setId("acc")

        self.le1.setText("1")
        self.le2.setText("1")
        self.accuracy.setText("1")

        #Дабваление в сетку
        self.myLayout.addWidget(self.text1, alignment=Qt.AlignmentFlag.AlignTop)
        self.myLayout.addWidget(self.le1, alignment=Qt.AlignmentFlag.AlignTop)
        self.myLayout.addWidget(self.text2, alignment=Qt.AlignmentFlag.AlignTop)
        self.myLayout.addWidget(self.le2, alignment=Qt.AlignmentFlag.AlignTop)
        self.myLayout.addWidget(self.text3, alignment=Qt.AlignmentFlag.AlignTop)
        self.myLayout.addWidget(self.accuracy, alignment=Qt.AlignmentFlag.AlignTop)
        self.myLayout.addWidget(self.cbab, alignment=Qt.AlignmentFlag.AlignTop)
        self.myLayout.addWidget(self.button_save, alignment=Qt.AlignmentFlag.AlignTop)
        self.myLayout.addWidget(self.button_info, alignment=Qt.AlignmentFlag.AlignTop)

        self.myLayout.addWidget(self.button_info, alignment=Qt.AlignmentFlag.AlignHCenter)

        self.le1.textChanged.connect(self.update_paint)
        self.le2.textChanged.connect(self.update_paint)
        self.accuracy.textChanged.connect(self.update_paint)
        self.cbab.stateChanged.connect(self.update_paint)
        self.button_save.clicked.connect(self.show_saved_win)

        #Пружина
        self.myLayout.addStretch()

    def create_settings_astroid(self):
        info = "<b>Астроида</b> - это кривая построенная качением окружности с радиусом r по внутренней стороне окружности радиусом 4*r.<br><br>a - множитель растягивающий график вдоль оси OX<br>b - множитель растягивающий график вдоль оси OY"
        
        #Параметры
        self.text1 = QtWidgets.QLabel("Параметр a:")
        self.le1 = MyLineEdit()
        self.text2 = QtWidgets.QLabel("Параметр b:")
        self.le2 = MyLineEdit()
        self.text3 = QtWidgets.QLabel("Точность:")
        self.accuracy = MyLineEdit()
        self.button_save = QtWidgets.QPushButton("Сохранить как...")
        self.button_info = MyButton("i")

        self.button_info.set_tt(shenter_text(info))
        self.button_info.setFixedSize(22, 22)

        self.le1.setId("param")
        self.le2.setId("param")
        self.accuracy.setId("acc")

        self.le1.setText("1")
        self.le2.setText("1")
        self.accuracy.setText("1")

        #Дабваление в сетку
        self.myLayout.addWidget(self.text1, alignment=Qt.AlignmentFlag.AlignTop)
        self.myLayout.addWidget(self.le1, alignment=Qt.AlignmentFlag.AlignTop)
        self.myLayout.addWidget(self.text2, alignment=Qt.AlignmentFlag.AlignTop)
        self.myLayout.addWidget(self.le2, alignment=Qt.AlignmentFlag.AlignTop)
        self.myLayout.addWidget(self.text3, alignment=Qt.AlignmentFlag.AlignTop)
        self.myLayout.addWidget(self.accuracy, alignment=Qt.AlignmentFlag.AlignTop)
        self.myLayout.addWidget(self.button_save, alignment=Qt.AlignmentFlag.AlignTop)
        self.myLayout.addWidget(self.button_info, alignment=Qt.AlignmentFlag.AlignTop)

        self.myLayout.addWidget(self.button_info, alignment=Qt.AlignmentFlag.AlignHCenter)

        self.le1.textChanged.connect(self.update_paint)
        self.le2.textChanged.connect(self.update_paint)
        self.accuracy.textChanged.connect(self.update_paint)
        self.button_save.clicked.connect(self.show_saved_win)

        #Пружина
        self.myLayout.addStretch()

    def create_settings_epicycloid(self):
        info = "<b>Эпициклоида</b> - это кривая построенная качением окружности по внешней стороне другой окружности.<br><br>a - радиус катящейся окружности<br>b - радиус окружности по которой катится другая"
        
        #Параметры
        self.text1 = QtWidgets.QLabel("Параметр a:")
        self.le1 = MyLineEdit()
        self.text2 = QtWidgets.QLabel("Параметр b:")
        self.le2 = MyLineEdit()
        self.text3 = QtWidgets.QLabel("Точность:")
        self.accuracy = MyLineEdit()
        self.button_save = QtWidgets.QPushButton("Сохранить как...")
        self.button_info = MyButton("i")

        self.button_info.set_tt(shenter_text(info))
        self.button_info.setFixedSize(22, 22)

        self.le1.setId("param")
        self.le2.setId("param")
        self.accuracy.setId("acc")

        self.le1.setText("1")
        self.le2.setText("1")
        self.accuracy.setText("1")

        #Дабваление в сетку
        self.myLayout.addWidget(self.text1, alignment=Qt.AlignmentFlag.AlignTop)
        self.myLayout.addWidget(self.le1, alignment=Qt.AlignmentFlag.AlignTop)
        self.myLayout.addWidget(self.text2, alignment=Qt.AlignmentFlag.AlignTop)
        self.myLayout.addWidget(self.le2, alignment=Qt.AlignmentFlag.AlignTop)
        self.myLayout.addWidget(self.text3, alignment=Qt.AlignmentFlag.AlignTop)
        self.myLayout.addWidget(self.accuracy, alignment=Qt.AlignmentFlag.AlignTop)
        self.myLayout.addWidget(self.button_save, alignment=Qt.AlignmentFlag.AlignTop)
        self.myLayout.addWidget(self.button_info, alignment=Qt.AlignmentFlag.AlignTop)

        self.myLayout.addWidget(self.button_info, alignment=Qt.AlignmentFlag.AlignHCenter)

        self.le1.textChanged.connect(self.update_paint)
        self.le2.textChanged.connect(self.update_paint)
        self.accuracy.textChanged.connect(self.update_paint)
        self.button_save.clicked.connect(self.show_saved_win)

        #Пружина
        self.myLayout.addStretch()

    def create_settings_hypocycloid(self):
        info = "<b>Гипоциклоида</b> - это кривая построенная качением окружности по внутренней стороне другой окружности.<br><br>a - радиус катящейся окружности<br>b - радиус окружности по которой катится другая"
        
        #Параметры
        self.text1 = QtWidgets.QLabel("Параметр a:")
        self.le1 = MyLineEdit()
        self.text2 = QtWidgets.QLabel("Параметр b:")
        self.le2 = MyLineEdit()
        self.text3 = QtWidgets.QLabel("Точность:")
        self.accuracy = MyLineEdit()
        self.button_save = QtWidgets.QPushButton("Сохранить как...")
        self.button_info = MyButton("i")

        self.button_info.set_tt(shenter_text(info))
        self.button_info.setFixedSize(22, 22)

        self.le1.setId("param")
        self.le2.setId("param")
        self.accuracy.setId("acc")

        self.le1.setText("1")
        self.le2.setText("3")
        self.accuracy.setText("1")

        #Дабваление в сетку
        self.myLayout.addWidget(self.text1, alignment=Qt.AlignmentFlag.AlignTop)
        self.myLayout.addWidget(self.le1, alignment=Qt.AlignmentFlag.AlignTop)
        self.myLayout.addWidget(self.text2, alignment=Qt.AlignmentFlag.AlignTop)
        self.myLayout.addWidget(self.le2, alignment=Qt.AlignmentFlag.AlignTop)
        self.myLayout.addWidget(self.text3, alignment=Qt.AlignmentFlag.AlignTop)
        self.myLayout.addWidget(self.accuracy, alignment=Qt.AlignmentFlag.AlignTop)
        self.myLayout.addWidget(self.button_save, alignment=Qt.AlignmentFlag.AlignTop)
        self.myLayout.addWidget(self.button_info, alignment=Qt.AlignmentFlag.AlignTop)

        self.myLayout.addWidget(self.button_info, alignment=Qt.AlignmentFlag.AlignHCenter)

        self.le1.textChanged.connect(self.update_paint)
        self.le2.textChanged.connect(self.update_paint)
        self.accuracy.textChanged.connect(self.update_paint)
        self.button_save.clicked.connect(self.show_saved_win)

        #Пружина
        self.myLayout.addStretch()

    #Обновление параметров
    def update_values(self):
        self.func.params = []
        for i in range(0, self.myLayout.count()):
            item = self.myLayout.itemAt(i)
            w = item.widget()
            if w.__class__.__name__ == "MyLineEdit" and w is not None:
                if w.getId() == "param":
                    self.func.params.append(float(w.text()))
            if w.__class__.__name__ == "QCheckBox" and w is not None:
                self.func.ab_mode = w.isChecked()

    #Обновление рисунка после смены данных в LineEdit
    def update_paint(self, ):
        if self.is_correct():
            self.update_values()
            self.child.clear_paint()
            self.child.PaintGraphic(float(self.accuracy.text()))

    #Закрытие окна графики
    def close_graphic(self):
        if self.child != 0:
            self.child.view.close()
            self.child = 0

    #Проверка на корректность данных
    def is_correct(self):
        for i in range(0, self.myLayout.count()):
            item = self.myLayout.itemAt(i)
            w = item.widget()
            if w.__class__.__name__ == "MyLineEdit" and w is not None:
                try:
                    float(w.text())
                    if w.getId() == "acc":
                        if float(w.text()) > 500 or float(w.text()) < 0:
                            return False 
                        a = 1/float(w.text())
                except ValueError:
                    return False
                except ZeroDivisionError:
                    return False
        return True
    
    def table_polar(self, file):
        if self.child.vr == "norm":
            pol = self.child.pol.polygon()
            cnt = pol.count()

            file.write("|---------|---------|\n")
            file.write("|    φ    |    r    |\n")
            file.write("|---------|---------|\n")

            for i in range(0, cnt):
                x = pol.at(i).x() - 1000
                y = 1000 - pol.at(i).y()

                den = sqrt(x**2 + y**2)

                if x == 0 and y == 0:
                    deg = 0
                elif y >= 0 and x >= 0:
                    deg = 0 + degrees(asin(y/den))
                elif y >= 0 and x <= 0:
                    deg = 180 - degrees(asin(y/den))
                elif y <= 0 and x <= 0:
                    deg = 180 - degrees(asin(y/den))
                else:
                    deg = 360 + degrees(asin(y/den))

                v = str(round(deg, 2))
                r = str(round(sqrt(x**2 + y**2)/10, 2))

                string = "|" + v + "°" + (8-len(v))*" " + "|" + r + (9-len(r))*" " + "|\n"

                file.write(string)
                file.write("|---------|---------|\n")

        elif self.child.vr == "pr":
            pol = self.child.pol.polygon()
            cnt = pol.count()

            accuracy = float(self.accuracy.text())

            k = 0
            step = 1/accuracy

            file.write("|---------|---------|\n")
            file.write("|    φ    |    r    |\n")
            file.write("|---------|---------|\n")

            for i in range(0, cnt):
                x = pol.at(i).x() - 1000
                y = 1000 - pol.at(i).y()

                den = sqrt(x**2 + y**2)

                v = str(k)
                r = str(round(sqrt(x**2 + y**2)/10, 2))

                string = "|" + v + "°" + (8-len(v))*" " + "|" + r + (9-len(r))*" " + "|\n"

                file.write(string)
                file.write("|---------|---------|\n")

                k += step

        elif self.child.vr == "sp":
            lines = self.child.lines
            cnt = len(lines)

            accuracy = float(self.accuracy.text())

            if float(self.le3.text()) <= float(self.le4.text()):
                k = float(self.le3.text())
            else:
                k = float(self.le4.text())

            step = 1/accuracy

            file.write("|---------|---------|\n")
            file.write("|    φ    |    r    |\n")
            file.write("|---------|---------|\n")

            for i in lines:
                line = i.line()

                x = line.x1() - 1000
                y = 1000 -line.y1()

                den = sqrt(x**2 + y**2)

                v = str(k)
                r = str(round(sqrt(x**2 + y**2)/10, 2))

                string = "|" + v + "°" + (8-len(v))*" " + "|" + r + (9-len(r))*" " + "|\n"

                file.write(string)

                k += step
            
            line = lines[-1].line()

            x = line.x2() - 1000
            y = 1000 -line.y2()
            den = sqrt(x**2 + y**2)

            v = str(k)
            r = str(round(sqrt(x**2 + y**2)/10, 2))

            string = "|" + v + "°" + (8-len(v))*" " + "|" + r + (9-len(r))*" " + "|\n"

            file.write(string)
            file.write("|---------|---------|\n")

        else:
            lines = self.child.lines
            cnt = len(lines)

            file.write("|---------|---------|\n")
            file.write("|    φ    |    r    |\n")
            file.write("|---------|---------|\n")

            for i in lines:
                line = i.line()

                x = line.x1() - 1000
                y = 1000 -line.y1()

                den = sqrt(x**2 + y**2)

                if x == 0 and y == 0:
                    deg = 0
                elif y >= 0 and x >= 0:
                    deg = 0 + degrees(asin(y/den))
                elif y >= 0 and x <= 0:
                    deg = 180 - degrees(asin(y/den))
                elif y <= 0 and x <= 0:
                    deg = 180 - degrees(asin(y/den))
                else:
                    deg = 360 + degrees(asin(y/den))

                v = str(round(deg, 2))
                r = str(round(sqrt(x**2 + y**2)/10, 2))

                string = "|" + v + "°" + (8-len(v))*" " + "|" + r + (9-len(r))*" " + "|\n"

                file.write(string)
                file.write("|---------|---------|\n")
                
    def table_param(self, file):
        if self.child.vr == "norm" or self.child.vr == "pr":
            pol = self.child.pol.polygon()
            cnt = pol.count()

            file.write("|---------|---------|\n")
            file.write("|    x    |    y    |\n")
            file.write("|---------|---------|\n")

            for i in range(0, cnt):
                x = str(round((pol.at(i).x() - 1000)/10, 2))
                y = str(round((1000 - pol.at(i).y())/10, 2))

                string = "|" + x + (9-len(x))*" " + "|" + y + (9-len(y))*" " + "|\n"

                file.write(string)
                file.write("|---------|---------|\n")

        elif self.child.vr == "ep":
            lines = self.child.lines
            cnt = len(lines)

            file.write("|---------|---------|\n")
            file.write("|    x    |    y    |\n")
            file.write("|---------|---------|\n")

            for i in lines:
                line = i.line()

                x = str(round((line.x1() - 1000)/10, 2))
                y = str(round((1000 - line.y1())/10, 2))

                string = "|" + x + (9-len(x))*" " + "|" + y + (9-len(y))*" " + "|\n"

                file.write(string)
            
            line = lines[-1].line()

            x = str(round((line.x2() - 1000)/10, 2))
            y = str(round((1000 - line.y2())/10, 2))

            string = "|" + x + (9-len(x))*" " + "|" + y + (9-len(y))*" " + "|\n"

            file.write(string)
            file.write("|---------|---------|\n")

        else:
            lines = self.child.lines
            cnt = len(lines)

            file.write("|---------|---------|\n")
            file.write("|    x    |    y    |\n")
            file.write("|---------|---------|\n")

            for i in lines:
                line = i.line()

                x = str(round((line.x1() - 1000)/10, 2))
                y = str(round((1000 - line.y1())/10, 2))

                string = "|" + x + (9-len(x))*" " + "|" + y + (9-len(y))*" " + "|\n"

                file.write(string)
                file.write("|---------|---------|\n")