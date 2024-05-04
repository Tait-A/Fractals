import numpy as np
from PIL import Image
from sets import Fractal, Mandelbrot


# A visualiser for fractals
class Visualiser:
    def __init__(self, fractal: Fractal) -> "Visualiser":
        self.fractal = fractal

    def display(self):
        output = self.fractal.generate()
        img = output
        print

        img = Image.fromarray(img)
        img.show()


if __name__ == "__main__":
    m = Mandelbrot(50, 10000)
    v = Visualiser(m)
    v.display()
