from PyQt6.QtWidgets import QGraphicsScene, QGraphicsView
from PyQt6.QtGui import QPen, QPolygonF, QFont, QColor, QIcon
from PyQt6.QtGui import QPainter
from PyQt6.QtCore import Qt
from PyQt6 import QtCore
from MyLib.ML import *

class WinPaintGraphics(QGraphicsScene):

    def __init__(self, parrent, func, ws, variant):       
        super().__init__()
        
        #Поля
        self.WIDTH_VIEW = 500
        self.HEIGHT_VIEW = 500
        self.WORKSPACE_WIDTH = 2000
        self.WORKSPACE_HEIGHT = 2000
        self.func = func
        self.par = parrent
        self.var = variant
        self.ws = ws
        self.vr = variant

        #Создание сцены
        self.setSceneRect(0, 0, self.WORKSPACE_WIDTH, self.WORKSPACE_HEIGHT)

        #Создание рабочего пространства
        match ws:
            case "polar":
                self.set_workspace_polar()
            case "param":
                self.set_workspace_dekart()

        #Настройка вьюшки
        self.view = Zoom_View(self)
        self.view.setGeometry(parrent.x + parrent.WIDTH, parrent.y, self.WIDTH_VIEW, self.HEIGHT_VIEW)
        self.view.setWindowFlags(self.view.windowFlags() & ~QtCore.Qt.WindowType.WindowCloseButtonHint)
        self.view.setWindowIcon(QIcon("icon.ico"))
        self.view.show()

        self.view.setRenderHints(QPainter.RenderHint.Antialiasing)

        self.PaintGraphic(float(parrent.accuracy.text()))

    #Создание рабочего декартового пространства
    def set_workspace_dekart(self):
        if is_dark_theme_enabled():
            pen = QPen(Qt.GlobalColor.darkGray)
            penOxy = QPen(Qt.GlobalColor.lightGray)
        else:
            pen = QPen(Qt.GlobalColor.lightGray)
            penOxy = QPen(Qt.GlobalColor.darkGray)

        for i in range(0, 200-1):
            self.addLine(self.WORKSPACE_WIDTH//200*(i+1), 0, self.WORKSPACE_WIDTH//200*(i+1), self.WORKSPACE_HEIGHT, pen)
        
        for i in range(0, 200-1):
            self.addLine(0, self.WORKSPACE_HEIGHT//200*(i+1), self.WORKSPACE_WIDTH, self.WORKSPACE_HEIGHT//200*(i+1), pen)

        self.addLine(0, self.WORKSPACE_HEIGHT//2, self.WORKSPACE_WIDTH, self.WORKSPACE_HEIGHT//2, penOxy)
        self.addLine(self.WORKSPACE_WIDTH//2, 0, self.WORKSPACE_WIDTH//2, self.WORKSPACE_HEIGHT, penOxy)

        font = QFont("Arial", 6)

        text1 = self.addText("1", font)
        text1.setPos(1004, 1000-5)
        text2 = self.addText("1", font)
        text2.setPos(1000-3, 1000-19)
        text3 = self.addText("-1", font)
        text3.setPos(1000-18, 1000-12)
        text4 = self.addText("-1", font)
        text4.setPos(1000-11, 1001)

    #Создание рабочего полярного пространства
    def set_workspace_polar(self):
        pen = QPen(Qt.GlobalColor.lightGray)

        self.addLine(0, self.WORKSPACE_HEIGHT//2, self.WORKSPACE_WIDTH, self.WORKSPACE_HEIGHT//2, pen)
        self.addLine(self.WORKSPACE_WIDTH//2, 0, self.WORKSPACE_WIDTH//2, self.WORKSPACE_HEIGHT, pen)
        self.addLine(self.WORKSPACE_WIDTH//2-self.WORKSPACE_HEIGHT//2, self.WORKSPACE_HEIGHT, self.WORKSPACE_WIDTH//2+self.WORKSPACE_HEIGHT//2, 0, pen)
        self.addLine(self.WORKSPACE_WIDTH//2-self.WORKSPACE_HEIGHT//2, 0, self.WORKSPACE_WIDTH//2+self.WORKSPACE_HEIGHT//2, self.WORKSPACE_HEIGHT, pen)

        for i in range(0, 10):
            self.addRect(self.WORKSPACE_WIDTH//2-100*(i+1), self.WORKSPACE_HEIGHT//2-100*(i+1), 200*(i+1), 200*(i+1), pen)

        font = QFont("Arial", 6)

        text1 = self.addText("0", font)
        text1.setPos(1060, 1000)
        text2 = self.addText("90", font)
        text2.setPos(1000, 1000-70)
        text3 = self.addText("180", font)
        text3.setPos(1000-70, 1000)
        text4 = self.addText("270", font)
        text4.setPos(1000, 1060)

        text11 = self.addText("10", font)
        text11.setPos(1000, 1000-115)
        text22 = self.addText("20", font)
        text22.setPos(1000, 1000-215)
        text33 = self.addText("30", font)
        text33.setPos(1000, 1000-315)
        text44 = self.addText("40", font)
        text44.setPos(1000, 1000-415)
        text55 = self.addText("50", font)
        text55.setPos(1000, 1000-515)
        text66 = self.addText("60", font)
        text66.setPos(1000, 1000-615)
        text77 = self.addText("70", font)
        text77.setPos(1000, 1000-715)
        text88 = self.addText("80", font)
        text88.setPos(1000, 1000-815)
        text99 = self.addText("90", font)
        text99.setPos(1000, 1000-915)
    
    #Нарисовать цикличный график
    def PaintGraphic(self, accuracy):
        if is_dark_theme_enabled():
            pen = QPen(QColor("yellow"))
        else:
            pen = QPen(QColor("black"))

        match self.var:
            case "norm":
                points = []
                accuracy = float(accuracy)

                for i in MyRange(0, 360, 1/accuracy):
                    points.append(self.func.get_point(i))

                self.pol = self.addPolygon(QPolygonF(points), pen)

            case "pr":
                points = []
                accuracy = float(accuracy)

                mult = float(self.par.le2.text())
                
                den = mult - int(mult)
                mod = get_mod(den)

                for i in MyRange(0, mod*360, 1/accuracy):
                    points.append(self.func.get_point(i))

                self.pol = self.addPolygon(QPolygonF(points), pen)

            case "nc":
                prev_point = None
                self.lines = []

                accuracy = float(accuracy)

                for i in MyRange(-90, 180, 1/accuracy):
                    point = self.func.get_point(i)

                    if point is not None and prev_point is not None:
                        self.lines.append(self.addLine(prev_point.x(), prev_point.y(), point.x(), point.y(), pen))

                    prev_point = point

            case "nncc":
                prev_point = None
                self.lines = []

                accuracy = float(accuracy)

                for i in MyRange(0, 360, 1/accuracy):
                    point = self.func.get_point(i)

                    if point is not None and prev_point is not None:
                        self.lines.append(self.addLine(prev_point.x(), prev_point.y(), point.x(), point.y(), pen))

                    prev_point = point

            case "sp":
                prev_point = None
                self.lines = []

                accuracy = float(accuracy)
                bord1 = float(self.par.le3.text())
                bord2 = float(self.par.le4.text())

                if bord1 <= bord2:
                    for i in MyRange(bord1, bord2, 1/accuracy):
                        point = self.func.get_point(i)

                        if point is not None and prev_point is not None:
                            self.lines.append(self.addLine(prev_point.x(), prev_point.y(), point.x(), point.y(), pen))

                        prev_point = point

                else:
                    for i in MyRange(bord2, bord1, 1/accuracy):
                        point = self.func.get_point(i)

                        if point is not None and prev_point is not None:
                            self.lines.append(self.addLine(prev_point.x(), prev_point.y(), point.x(), point.y(), pen))

                        prev_point = point
            
            case "ep":
                prev_point = None
                accuracy = float(accuracy)
                self.lines = []

                mod = 1

                if float(self.par.le1.text()) != 0:
                    mult = float(self.par.le2.text())/float(self.par.le1.text())
                
                    den = mult - int(mult)
                    mod = get_mod(den)

                for i in MyRange(0, mod*360, 1/accuracy):
                    point = self.func.get_point(i)

                    if point is not None and prev_point is not None:
                        self.lines.append(self.addLine(prev_point.x(), prev_point.y(), point.x(), point.y(), pen))

                    prev_point = point

    #Стереть рисунок
    def clear_paint(self):
        match self.var:
            case "norm":
                self.removeItem(self.pol)
            case "pr":
                self.removeItem(self.pol)
            case "nc":
                for i in self.lines:
                    self.removeItem(i)
            case "sp":
                for i in self.lines:
                    self.removeItem(i)
            case "nncc":
                for i in self.lines:
                    self.removeItem(i)
            case "ep":
                for i in self.lines:
                    self.removeItem(i)

#Вьюшка
class Zoom_View(QGraphicsView):
    def __init__(self, par):
        super().__init__(par)
        self._is_drag = False
    
    #Масштабирование
    def wheelEvent(self, event):
        if event.angleDelta().y() < 0:
            self.scale(0.83, 0.83)
        elif event.angleDelta().y() > 0:
            self.scale(1.2, 1.2)

    #Премещение: определение захвата
    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            self._is_drag = True
            self._posMouse = event.pos()

    #Перемещение: дельты и смещение
    def mouseMoveEvent(self, event):
        if self._is_drag:
            self._posDeltaMouse = event.pos()
        
            dx = self._posDeltaMouse.x() - self._posMouse.x()
            dy = self._posDeltaMouse.y() - self._posMouse.y()

            self.horizontalScrollBar().setValue(self.horizontalScrollBar().value() - dx)
            self.verticalScrollBar().setValue(self.verticalScrollBar().value() - dy)

            self._posMouse = self._posDeltaMouse

    #Перемещение: определение отпускания
    def mouseReleaseEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            self._is_drag = False