import sys
from PyQt5.QtGui import QPainter, QImage, QColor
from PyQt5.QtCore import QRectF, Qt
from PyQt5.QtWidgets import QApplication, QGraphicsView, QGraphicsScene, QGraphicsItem
import numpy as np
from sets import Fractal, Mandelbrot, Julia


# This is the core item that contains the fractal
class FractalItem(QGraphicsItem):
    def __init__(self, rect: QRectF, size, fractal: Fractal):
        super().__init__()
        self.rect = rect
        self.size = size
        self.fractal = fractal

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
        iters = int(100 / np.sqrt(width))
        Z = self.fractal.generate(iters, C)

        image = QImage(
            self.image_size.width(), self.image_size.height(), QImage.Format_RGB32
        )
        for i in range(self.image_size.height()):
            for j in range(self.image_size.width()):
                color = 255 - Z[i, j]
                image.setPixel(j, i, QColor(color, color, color).rgb())

        painter.drawImage(self.rect.topLeft(), image)


class Scrollable(QGraphicsView):
    def __init__(self, scene):
        super().__init__(scene)
