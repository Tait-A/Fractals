import numpy as np
from PIL import Image
from src.sets import Fractal, Mandelbrot, Julia
from typing import List, Optional
from src.colourmap import ColourMap, Colour
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



def parse(julia: bool = False) -> tuple[Optional[float], Optional[float], ColourMap]:
    parser = argparse.ArgumentParser(description="Visualise fractals.")

    if julia:
        parser.add_argument(
            "--real", type=float, required=False, help="Real part of the complex number. [-1,1]"
        )
        parser.add_argument(
            "--imag", type=float, required=False, help="Imaginary part of the complex number. [-1,1]"
        )

    parser.add_argument(
        "--colours", help="Select the colours you use interactively.", action="store_true"
    )

    args = parser.parse_args()

    if julia:
        if args.real is not None:
            real = args.real
        else:
            real = random.uniform(-1, 1)
        if args.imag is not None:
            imaginary = args.imag
        else:
            imaginary = random.uniform(-1, 1)
    else:
        real = None
        imaginary = None

    if args.colours:
        colours = get_colours()
    else:
        no_colours = random.randint(2, 4)
        colours = [random.choice(list(Colour)) for _ in range(no_colours)]

    colourmap = ColourMap(colours, "rgb")
    print(f"Using colours: {[colour.name for colour in colours]}")
    if julia:
        print(f"Real part: {real}, Imaginary part: {imaginary}")

    return real, imaginary, colourmap


def get_colours() -> List[Colour]:
    """Get a list of colours from the user."""
    colours = []
    print("Enter the colours you want to use (e.g. 'red', 'green', 'blue'). \nType 'done' when finished. \nType 'help' for a list of available colours.")
    while True:
        colour = input("Colour: ")
        if colour.lower() == "done":
            break
        if colour.lower() == "help":
            print("Available colours: ", [colour.name for colour in Colour])
            continue
        try:
            colours.append(Colour[colour.upper()])
        except KeyError:
            print(f"'{colour}' is not a valid colour. Please try again.")
    return colours


def julia() -> None:
    """Visualise a Julia set."""
    real, imaginary, colourmap = parse(julia=True)

    c = complex(real, imaginary)
    j = Julia(c, 100, 1000)
    v = Visualiser(j, smoothing=True, colourmap=colourmap)

    v.display()


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
