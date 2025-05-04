import numpy as np
from math import log


class Fractal:
    def __init__(self, max_iterations, pixel_density, width=2, height=2) -> "Fractal":
        self.max_iterations = max_iterations
        self.output = np.zeros(
            (height * pixel_density, width * pixel_density), dtype=np.uint8
        )
        self.matrix = self.complex_mat(width, height, pixel_density)

    def complex_mat(self, width, height, pixel_density) -> np.ndarray:
        re = np.linspace(-width, width, width * pixel_density)
        im = np.linspace(-height, height, height * pixel_density)
        return re[np.newaxis, :] + im[:, np.newaxis] * 1j

    def generate(
        self, iterations: int = None, matrix: np.ndarray = None, smoothing: bool = False
    ) -> np.ndarray:
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

    def stability(self, c: complex) -> int:
        divergence = self.divergence(c)
        return max(0.0, min(1.0, (divergence / self.max_iterations)))

    def generate(
        self, iterations: int = None, matrix: np.ndarray = None, smoothing: bool = False
    ) -> np.ndarray:
        if iterations is None:
            iterations = self.max_iterations
        if matrix is None:
            matrix = self.matrix
        z = np.zeros_like(matrix, dtype=np.complex64)
        output = np.zeros_like(matrix, dtype=np.float32)

        for i in range(iterations):
            mask = np.abs(z) <= 2
            z[mask] = z[mask] * z[mask] + matrix[mask]
            output[mask] = i

        if smoothing:
            mask = np.abs(z) > 2
            output[mask] += 1 - np.log(np.log(np.abs(z[mask]))) / np.log(2)
            output[~mask] = iterations

        self.output = np.clip(output / iterations, 0, 1)
        return self.output

    def __contains__(self, c: complex) -> bool:
        return ~(self.stability(c) < 1)


class Julia(Fractal):
    def __init__(
        self, c: complex, max_iterations, pixel_density, width=2, height=2
    ) -> "Julia":
        super().__init__(max_iterations, pixel_density, width, height)
        self.c = c

    def sequence(self, z: complex):
        while True:
            z = z * z + self.c
            yield z

    def divergence(self, z: complex):
        for i, z in enumerate(self.sequence(z)):
            if abs(z) > 2:
                return i + 1 - log(log(abs(z))) / log(2)
            if i >= self.max_iterations:
                return self.max_iterations

    def stability(self, z: complex) -> int:
        divergence = self.divergence(z)
        return max(0.0, min(1.0, (divergence / self.max_iterations)))

    def generate(
        self, iterations: int = None, matrix: np.ndarray = None, smoothing: bool = False
    ) -> np.ndarray:
        if iterations is None:
            iterations = self.max_iterations
        if matrix is None:
            matrix = self.matrix
        z = matrix
        output = np.zeros_like(matrix, dtype=np.float32)

        for i in range(iterations):
            mask = np.abs(z) <= 2
            z[mask] = z[mask] * z[mask] + self.c
            output[mask] = i

        if smoothing:
            mask = np.abs(z) > 2
            output[mask] += 1 - np.log(np.log(np.abs(z[mask]))) / np.log(2)
            output[~mask] = iterations

        self.output = np.clip(output / iterations, 0, 1)
        return self.output


if __name__ == "__main__":
    c = complex(0, 0)
    j = Julia(c, 100, 10)
    m = Mandelbrot(100, 100)
    print()
