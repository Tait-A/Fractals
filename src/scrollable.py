import sys
from PyQt5.QtGui import QPainter, QImage, QColor
from PyQt5.QtCore import QRectF, Qt, QSize
from PyQt5.QtWidgets import (
    QApplication,
    QGraphicsView,
    QGraphicsScene,
    QGraphicsItem,
    QMainWindow,
)
import numpy as np
from sets import Fractal, Mandelbrot, Julia
import matplotlib.pyplot as plt
from colourmap import ColorMap, Color
from PIL import Image


# This is the core item that contains the fractal
class FractalItem(QGraphicsItem):
    def __init__(self, rect: QRectF, size: QSize, fractal: Fractal):
        super().__init__()
        self.rect = rect
        self.size = size
        self.fractal = fractal

    def boundingRect(self):
        return self.rect

    def paint(self, painter, size, widget):
        x0, y0, width, height = (
            self.rect.left(),
            self.rect.top(),
            self.rect.width(),
            self.rect.height(),
        )

        x = np.linspace(x0, x0 + width, self.size.width())
        y = np.linspace(y0, y0 + height, self.size.height())
        print("x: ", x)
        print("y: ", y)
        print("width: ", width)
        print("height: ", height)
        X, Y = np.meshgrid(x, y)
        C = X + Y * 1j
        # print(C)
        iters = int(100 / np.sqrt(width))
        Z = self.fractal.generate(iters, C)
        # print(Z)
        # img = Image.fromarray(Z)
        # img.show()
        Z = self.get_colour(Z)

        image = QImage(self.size.width(), self.size.height(), QImage.Format_RGB32)
        for i in range(self.size.height()):
            for j in range(self.size.width()):
                color = Z[i, j]
                image.setPixelColor(j, i, color)

        painter.drawImage(self.rect.topLeft(), image)

    def get_colour(self, input: np.ndarray, cmap_name="hot") -> np.ndarray:
        "Convert the values in the matrix from (0,1) to a Qcolor object"
        cmap = ColorMap()
        qcolors = cmap(input)
        return qcolors


class Scrollable(QMainWindow):
    def __init__(self, fractal):
        super().__init__()
        self.scene = QGraphicsScene()
        self.view = QGraphicsView(self.scene, self)
        self.setCentralWidget(self.view)

        # The coordinates for the Mandelbrot set and the size of the image
        self.mandelbrotItem = FractalItem(
            QRectF(-2.0, -1.5, 3.0, 3.0), QSize(800, 600), fractal
        )
        self.scene.addItem(self.mandelbrotItem)
        self.view.fitInView(self.mandelbrotItem, Qt.KeepAspectRatio)

        # Enable dragging and scroll bars
        self.view.setDragMode(QGraphicsView.ScrollHandDrag)
        self.view.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        self.view.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)

        self.setWindowTitle("Mandelbrot Set Viewer")
        self.setGeometry(100, 100, 600, 800)

    def wheelEvent(self, event):
        # Zoom in or out when the mouse wheel is used
        factor = 1.1 if event.angleDelta().y() > 0 else 0.9
        self.view.scale(factor, factor)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    fractal = Mandelbrot(100, 100)
    main_win = Scrollable(fractal)
    main_win.show()
    sys.exit(app.exec_())
