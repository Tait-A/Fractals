import numpy as np
from PIL import Image
from sets import Fractal, Mandelbrot, Julia
from dataclasses import dataclass
import matplotlib.pyplot as plt


# A visualiser for fractals
class Visualiser:
    def __init__(self, fractal: Fractal, smoothing: bool = False) -> "Visualiser":
        self.fractal = fractal
        self.smoothing = smoothing

    def display(self):
        img = self.fractal.generate(smoothing=self.smoothing)
        img = self.get_colour(img)
        img = Image.fromarray(img)
        img.show()

    def set_smoothing(self, smoothing: bool):
        self.smoothing = smoothing

    def get_colour(self, input: np.ndarray, cmap_name="hot"):
        """Convert a value in the range 0 to 1 to an RGB color from the given colormap."""
        cmap = plt.get_cmap(cmap_name)  # Get the colormap
        rgba = cmap(input)  # Get RGBA value from the colormap
        return np.uint8(rgba[..., :3] * 255)


@dataclass
class Viewer:
    image: Image
    centre: complex
    width: float

    @property
    def scale(self):
        return self.width / self.image.width

    @property
    def height(self):
        return self.image.height * self.scale

    @property
    def top_left(self):
        return self.centre + complex(-self.width, self.height) / 2

    def __iter__(self):
        for y in range(self.image.height):
            for x in range(self.image.width):
                yield Pixel(self, x, y)


@dataclass
class Pixel:
    viewer: Viewer
    x: int
    y: int

    @property
    def colour(self):
        return self.viewer.image.getpixel((self.x, self.y))

    @colour.setter
    def colour(self, value):
        self.viewer.image.putpixel((self.x, self.y), value)

    def c(self):
        return self.viewer.top_left + complex(self.x, -self.y) * self.viewer.scale


if __name__ == "__main__":
    m = Mandelbrot(50, 100)
    c = complex(0.28, 0.008)
    j = Julia(c, 100, 1000)
    v = Visualiser(j, smoothing=True)
    v.display()
