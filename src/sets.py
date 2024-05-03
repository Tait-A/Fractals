import numpy as np
from math import log


class Fractal:
    def __init__(self, max_iterations, pixel_density, width=2, height=2) -> "Fractal":
        self.max_iterations = max_iterations
        self.output = np.zeros(
            (height * pixel_density, width * pixel_density), dtype=np.uint8
        )
        self.matrix = self.complex_mat(width, height, pixel_density)

    def complex_mat(self, width, height, pixel_density):
        re = np.linspace(-width / 2, width / 2, width * pixel_density)
        im = np.linspace(-height / 2, height / 2, height * pixel_density)
        return re[np.newaxis, :] + im[:, np.newaxis] * 1j


class Mandelbrot(Fractal):
    def __init__(
        self, max_iterations, pixel_density, width=2, height=2
    ) -> "Mandelbrot":
        super().__init__(max_iterations, pixel_density, width, height)

    def sequence(self, c: complex, z: complex = 0):
        while True:
            z = z * z + c
            yield z

    def divergence(self, c):
        z = 0
        for i, z in enumerate(self.sequence(c)):
            print(i, z)
            if abs(z) > 2:
                return i + 1 - log(log(abs(z))) / log(2)
            if i >= self.max_iterations:
                return self.max_iterations

    def generate(self):
        for i, row in enumerate(self.matrix):
            for j, c in enumerate(row):
                self.output[i, j] = self.stability(c)
        return self.output

    def stability(self, c):
        divergence = self.divergence(c)
        return max(0.0, min(1.0, divergence / self.max_iterations))

    def __contains__(self, c: complex) -> bool:
        return ~(self.stability(c) < self.max_iterations)


if __name__ == "__main__":
    m = Mandelbrot(100, 100)
    print()
