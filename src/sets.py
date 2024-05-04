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
        re = np.linspace(-width, width, width * pixel_density)
        im = np.linspace(-height, height, height * pixel_density)
        return re[np.newaxis, :] + im[:, np.newaxis] * 1j

    def generate(self):
        raise NotImplementedError


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
            if abs(z) > 2:
                return i + 1 - log(log(abs(z))) / log(2)
            if i >= self.max_iterations:
                return self.max_iterations

    def stability(self, c):
        divergence = self.divergence(c)
        return max(0.0, min(1.0, (divergence / self.max_iterations)))

    def generate(self, smoothing: bool = False):
        z = np.zeros_like(self.matrix, dtype=np.complex64)
        output = np.zeros(self.matrix.shape, dtype=np.float32)

        for i in range(self.max_iterations):
            mask = np.abs(z) <= 2
            z[mask] = z[mask] * z[mask] + self.matrix[mask]
            output[mask] = i

        if smoothing:
            output = output + 1 - np.log(np.log(np.abs(z))) / np.log(2)
            # mask for output is not a number
            mask = np.isnan(output)
            output[mask] = self.max_iterations
        self.output = np.uint8(np.clip(output / self.max_iterations, 0, 1) * 255)
        return self.output

    def __contains__(self, c: complex) -> bool:
        return ~(self.stability(c) < self.max_iterations)


if __name__ == "__main__":
    m = Mandelbrot(100, 100)
    print()