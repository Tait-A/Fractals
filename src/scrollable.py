import sys
from PyQt5.QtGui import QPainter, QImage, QColor
from PyQt5.QtCore import QRectF, Qt
from PyQt5.QtWidgets import QApplication, QGraphicsView, QGraphicsScene, QGraphicsItem
import numpy as np
from sets import Fractal, Mandelbrot


class FractalItem(QGraphicsItem):
    def __init__(self, rect: QRectF, size, fractal: Fractal):
        super().__init__()
        self.rect = rect
        self.size = size

    def boundingRect(self):
        return self.rect

    def paint(self, painter, option, widget):
        x0, y0, width, height = (
            self.rect.left(),
            self.rect.top(),
            self.rect.width(),
            self.rect.height(),
        )
        x = np.linspace(x0, x0 + width, self.size[0])
        y = np.linspace(y0, y0 + height, self.size[1])
        X, Y = np.meshgrid(x, y)
        C = X + Y * 1j
        Z = np.zeros_like(C)


class Scrollable(QGraphicsView):
    def __init__(self, scene):
        super().__init__(scene)
