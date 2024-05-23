from enum import Enum
from typing import List, Union, Tuple
import numpy as np
from PyQt5.QtGui import QColor as Qcolor
import warnings

""" Custom colourmaps for use with Fractal Visualiser"""


class Color(Enum):
    RED = (255, 0, 0)
    GREEN = (0, 255, 0)
    BLUE = (0, 0, 255)
    YELLOW = (255, 255, 0)
    CYAN = (0, 255, 255)
    MAGENTA = (255, 0, 255)
    WHITE = (255, 255, 255)
    BLACK = (0, 0, 0)
    ORANGE = (255, 165, 0)
    PURPLE = (127, 0, 127)
    PINK = (255, 191, 203)


class ColorMap:
    def __init__(
        self, colors: List[Color] = [Color.RED, Color.MAGENTA], output_type: str = "Qt"
    ) -> "ColorMap":
        self.n = 256
        self.colors = colors

        match output_type:
            case "Qt":
                self.output_type = output_type
            case "matplotlib":
                self.output_type = output_type
            case "rgb":
                self.output_type = output_type
            case _:
                raise ValueError("Output type must be 'Qt', 'matplotlib' or 'rgb'")

        self.map = self.create_colormap(colors)

    def gradient(self, start: Color, end: Color, n: int) -> np.ndarray[Tuple]:
        "Return a list of n colors between start and end"
        r0, g0, b0 = start.value
        r1, g1, b1 = end.value

        i = np.arange(n)
        r = r0 + (r1 - r0) * i // (n - 1)
        g = g0 + (g1 - g0) * i // (n - 1)
        b = b0 + (b1 - b0) * i // (n - 1)

        return np.array([(rr, gg, bb) for rr, gg, bb in zip(r, g, b)])

    def create_colormap(self, colors: List[Color]) -> np.ndarray[Tuple]:
        "Create a colormap from a list of colors"
        n = len(colors)
        gradient = []
        for i in range(n - 1):
            gradient.extend(self.gradient(colors[i], colors[i + 1], self.n // (n - 1)))
        self.n = len(gradient)
        return np.array(gradient)

    def __call__(
        self, input: Union[float, np.ndarray]
    ) -> Union[Qcolor, np.ndarray[Qcolor]]:
        if isinstance(input, float):
            return self._eval(input)
        elif isinstance(input, np.ndarray):
            return self._eval_matrix(input)

    def _eval_matrix(self, values: np.ndarray[float]) -> np.ndarray[Qcolor]:
        if np.any(values < 0) or np.any(values > 1):
            warnings.warn("Values must be between 0 and 1. May have unintended results")
            values = np.clip(values, 0, 1)
        indices = (values * (self.n - 1)).astype(int)
        colors = self.map[indices]
        if self.output_type == "Qt":

            def to_qcolor(color):
                return Qcolor(*color)

            qcolors = np.apply_along_axis(to_qcolor, -1, colors)
            return qcolors
        elif self.output_type == "matplotlib":
            return colors / 256
        return colors

    def _eval(self, value: float) -> Qcolor:
        if value < 0 or value > 1:
            raise ValueError("Value must be between 0 and 1")
        index = int(value * (self.n - 1))
        color = self.map[index]
        if self.output_type == "Qt":
            return Qcolor(*color)
        elif self.output_type == "matplotlib":
            return color / 256
        return color


if __name__ == "__main__":
    import matplotlib.pyplot as plt

    cmap = ColorMap([Color.RED, Color.GREEN, Color.BLUE], "matplotlib")

    x = np.linspace(0, 1, 100)
    y = (np.sin(2 * np.pi * x) + 1) * 0.5

    colors = cmap(y)
    plt.scatter(x, y, c=colors)
    plt.show()
