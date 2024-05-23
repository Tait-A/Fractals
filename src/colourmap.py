from enum import Enum
from typing import List, Union
import numpy as np
from PyQt5.QtGui import QColor as Qcolor
import warnings

""" Custom colourmaps for use with Fractal Visualiser"""


class Color(Enum):
    RED = (256, 0, 0)
    GREEN = (0, 256, 0)
    BLUE = (0, 0, 256)
    YELLOW = (256, 256, 0)
    CYAN = (0, 256, 256)
    MAGENTA = (256, 0, 256)
    WHITE = (256, 256, 256)
    BLACK = (0, 0, 0)
    ORANGE = (256, 165, 0)
    PURPLE = (128, 0, 128)
    PINK = (256, 192, 203)

    def __init__(self, r, g, b):
        self.rgb = (r, g, b)


class ColorMap:
    def __init__(self, colors: List[Color] = [Color.RED, Color.MAGENTA]) -> "ColorMap":
        self.n = 256
        self.colors = colors
        self.map = self.create_colormap(colors)

    def gradient(self, start: Color, end: Color, n: int) -> np.ndarray[Color]:
        "Return a list of n colors between start and end"
        r0, g0, b0 = start.rgb
        r1, g1, b1 = end.rgb

        i = np.arange(n)
        r = r0 + (r1 - r0) * i // (n - 1)
        g = g0 + (g1 - g0) * i // (n - 1)
        b = b0 + (b1 - b0) * i // (n - 1)

        return np.array([Color(rr, gg, bb) for rr, gg, bb in zip(r, g, b)])

    def create_colormap(self, colors: List[Color]) -> np.ndarray[Color]:
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
        values = self.map[indices]
        qcolors = np.vectorize(lambda value: Qcolor(*value.rgb))
        return qcolors(values)

    def _eval(self, value: float) -> Qcolor:
        if value < 0 or value > 1:
            raise ValueError("Value must be between 0 and 1")
        index = int(value * (self.n - 1))
        return Qcolor(*self.map[index].rgb)
