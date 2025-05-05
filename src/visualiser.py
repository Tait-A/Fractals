import numpy as np
from PIL import Image
from sets import Fractal, Mandelbrot, Julia
from colourmap import ColourMap, Colour
import argparse
import random


# A visualiser for fractals
class Visualiser:
    def __init__(self, fractal: Fractal, smoothing: bool = False, colourmap = ColourMap([Colour.PURPLE, Colour.RED, Colour.BLACK], "rgb")) -> "Visualiser":
        self.fractal = fractal
        self.smoothing = smoothing
        self.colourmap = colourmap

    def display(self, iterations=None, matrix=None):
        img = self.fractal.generate(
            iterations=iterations, matrix=matrix, smoothing=self.smoothing
        )
        img = self.colourmap(img)
        img = Image.fromarray(img)
        img.show()

    def set_smoothing(self, smoothing: bool):
        self.smoothing = smoothing


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Visualise fractals.")
    parser.add_argument("--real", type=float, required=False, help="Real part of the complex number.")
    parser.add_argument("--imag", type=float, required=False, help="Imaginary part of the complex number.")
    args = parser.parse_args()

    real = args.real
    imaginary = args.imag

    if real is None:
        real = random.uniform(-1, 1)

    if imaginary is None:
        imaginary = random.uniform(-1, 1)

    no_colours = random.randint(2, 4)
    colours = [random.choice(list(Colour)) for _ in range(no_colours)]
    colourmap = ColourMap(colours, "rgb")
    print(f"Using colours: {colours}")
    print(f"Real part: {real}, Imaginary part: {imaginary}")

    c = complex(real, imaginary)
    j = Julia(c, 100, 1000)
    v = Visualiser(j, smoothing=True, colourmap=colourmap)

    x = np.linspace(-1, 1, 5000)
    y = np.linspace(-1, 1, 5000)
    matrix = x[np.newaxis, :] + y[:, np.newaxis] * 1j

    v.display()
