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
        self.colormap = ColorMap([Color.RED, Color.CYAN, Color.WHITE], "rgb")

    def display(self, iterations=None, matrix=None):
        img = self.fractal.generate(
            iterations=iterations, matrix=matrix, smoothing=self.smoothing
        )
        img = self.get_colour(img)
        print(img.shape)
        img = Image.fromarray(img)
        img.show()

    def set_smoothing(self, smoothing: bool):
        self.smoothing = smoothing

    def get_colour(self, input: np.ndarray, cmap_name="hot"):
        """Convert a value in the range 0 to 1 to an RGB color from the given colormap."""

        return self.colormap(input)


if __name__ == "__main__":
    m = Mandelbrot(20, 100)
    c = complex(0.28, 0.008)
    j = Julia(c, 100, 1000)
    v = Visualiser(m, smoothing=False)

    x = np.linspace(-1, 1, 5000)
    y = np.linspace(-1, 1, 5000)

    matrix = x[np.newaxis, :] + y[:, np.newaxis] * 1j

    v.display()
