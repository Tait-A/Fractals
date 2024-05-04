import numpy as np
from PIL import Image
from sets import Fractal, Mandelbrot


# A visualiser for fractals
class Visualiser:
    def __init__(self, fractal: Fractal, smoothing: bool = False) -> "Visualiser":
        self.fractal = fractal
        self.smoothing = smoothing

    def display(self):
        img = self.fractal.generate(self.smoothing)
        img = Image.fromarray(img)
        img.show()

    def set_smoothing(self, smoothing: bool):
        self.smoothing = smoothing


if __name__ == "__main__":
    m = Mandelbrot(50, 10000)
    v = Visualiser(m, smoothing=True)
    v.display()
