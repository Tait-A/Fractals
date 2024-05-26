import numpy as np
from PIL import Image
from sets import Fractal, Mandelbrot, Julia
from dataclasses import dataclass
import matplotlib.pyplot as plt
from colourmap import ColorMap, Color


# A visualiser for fractals
class Visualiser:
    def __init__(self, fractal: Fractal, smoothing: bool = False) -> "Visualiser":
        self.fractal = fractal
        self.smoothing = smoothing
        self.colormap = ColorMap([Color.PURPLE, Color.RED, Color.BLACK], "rgb")

    def display(self, iterations=None, matrix=None):
        img = self.fractal.generate(
            iterations=iterations, matrix=matrix, smoothing=self.smoothing
        )
        img = self.colormap(img)
        img = Image.fromarray(img)
        img.show()

    def set_smoothing(self, smoothing: bool):
        self.smoothing = smoothing


if __name__ == "__main__":
    m = Mandelbrot(60, 1000)
    c = complex(0.28, 0.008)
    j = Julia(c, 100, 10000)
    v = Visualiser(j, smoothing=True)

    x = np.linspace(-1, 1, 5000)
    y = np.linspace(-1, 1, 5000)
    matrix = x[np.newaxis, :] + y[:, np.newaxis] * 1j

    v.display()
