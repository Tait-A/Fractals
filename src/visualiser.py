import numpy as np
from PIL import Image
from sets import Fractal, Mandelbrot


# A visualiser for fractals
class Visualiser:
    def __init__(self, fractal: Fractal) -> "Visualiser":
        self.fractal = fractal

    def display(self):
        output = self.fractal.generate()
        img = np.zeros_like(output)
        for i in range(output.shape[0]):
            for j in range(output.shape[1]):
                img[i, j] = (1 - output[i, j]) * 255

        img = Image.fromarray(img)
        img.show()
