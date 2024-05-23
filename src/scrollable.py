import sys
from PyQt5.QtGui import QPainter, QImage, QColor
from PyQt5.QtCore import QRectF, Qt, QSize
from PyQt5.QtWidgets import (
    QApplication,
    QGraphicsView,
    QGraphicsScene,
    QGraphicsItem,
    QMainWindow,
    QWidget,
)
import numpy as np
from sets import Fractal, Mandelbrot, Julia
import matplotlib.pyplot as plt
from colourmap import ColorMap, Color
from PIL import Image


# This is the core item that contains the fractal
class FractalItem(QGraphicsItem):
    def __init__(self, size: QSize, bounds: QRectF, fractal: Fractal):
        super().__init__()
        self.rect = QRectF(0, 0, size.width(), size.height())
        self.size = size
        self.bounds = bounds
        self.fractal = fractal

    def boundingRect(self):
        return self.rect

    def complex_mat(self, x1, x2, y1, y2, x_pixels, y_pixels):
        re = np.linspace(x1, x2, x_pixels)
        im = np.linspace(y1, y2, y_pixels)
        return re[np.newaxis, :] + im[:, np.newaxis] * 1j

    def paint(self, painter, option, widget):
        x0, y0, width, height = (
            self.bounds.left(),
            self.bounds.top(),
            self.bounds.width(),
            self.bounds.height(),
        )

        C = self.complex_mat(
            x0, x0 + width, y0, y0 + height, self.size.width(), self.size.height()
        )

        iters = int(100 / np.sqrt(width))
        Z = self.fractal.generate(iters, C, True)
        Z = self.get_colour(Z)

        image = QImage(self.size.width(), self.size.height(), QImage.Format_RGB32)
        for i in range(self.size.height()):
            for j in range(self.size.width()):
                color = Z[i, j]
                image.setPixelColor(j, i, color)

        painter.drawImage(self.rect.topLeft(), image)

    def get_colour(self, input: np.ndarray, cmap_name="hot") -> np.ndarray:
        "Convert the values in the matrix from (0,1) to a Qcolor object"
        cmap = ColorMap([Color.RED, Color.BLACK])
        qcolors = cmap(input)
        return qcolors

    def update_bounds(self, bounds: QRectF):
        self.bounds = bounds
        self.update()


class MandelbrotViewer(QMainWindow):
    def __init__(self, fractal):
        super().__init__()

        self.scene = QGraphicsScene(self)
        self.view = QGraphicsView(self.scene)
        self.setCentralWidget(self.view)

        self.bounds = QRectF(-2, -1.5, 3, 3)
        # Define the Mandelbrot item
        self.mandelbrotItem = FractalItem(QSize(800, 600), self.bounds, fractal)
        self.scene.addItem(self.mandelbrotItem)

        # Set the scene rectangle to match the item
        self.scene.setSceneRect(self.mandelbrotItem.boundingRect())

        self.view.setRenderHint(QPainter.Antialiasing)
        self.view.fitInView(self.scene.sceneRect(), Qt.KeepAspectRatio)

        self.setWindowTitle("Mandelbrot Set Viewer")
        self.setGeometry(0, 0, 800, 600)

        # Enable zoom functionality
        self.view.setDragMode(QGraphicsView.ScrollHandDrag)
        self.view.setTransformationAnchor(QGraphicsView.AnchorUnderMouse)
        self.view.setResizeAnchor(QGraphicsView.AnchorUnderMouse)

    def wheelEvent(self, event):
        # Zoom in or out when the mouse wheel is used
        zoom_factor = 1.25
        if event.angleDelta().y() > 0:
            scale_factor = zoom_factor
        else:
            scale_factor = 1 / zoom_factor

        self.view.scale(scale_factor, scale_factor)
        self.update_bounds()

    def update_bounds(self):
        # Get the current view rectangle in scene coordinates
        view_rect = self.view.mapToScene(self.view.viewport().geometry()).boundingRect()

        # Map the view rectangle to the mathematical coordinates
        scene_width, scene_height = self.scene.width(), self.scene.height()
        bounds_width, bounds_height = self.bounds.width(), self.bounds.height()

        new_x = self.bounds.left() + (view_rect.left() / scene_width) * bounds_width
        new_y = self.bounds.top() + (view_rect.top() / scene_height) * bounds_height
        new_width = (view_rect.width() / scene_width) * bounds_width
        new_height = (view_rect.height() / scene_height) * bounds_height

        new_bounds = QRectF(new_x, new_y, new_width, new_height)
        self.mandelbrotItem.update_bounds(new_bounds)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    fractal = Mandelbrot(100, 1000)
    main_win = MandelbrotViewer(fractal)
    main_win.show()
    sys.exit(app.exec_())
