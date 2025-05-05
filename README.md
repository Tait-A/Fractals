## TAIT-A's Fractals

### A repository for visualising mandelbrot and julia sets

To run install pixi: https://pixi.sh/dev/

And then run with:
```pixi install && pixi run julia```

This will generate a random Julia set, to specify the complex number use the args '--real' and '--imag':
```pixi run julia --real 0.28 --image 0.008```

The colour gradient can be set by passing a list of colours to the ColourMap constructor, and this can then be applied to the fractal by passing the colourmap to the visualiser.

The output will be opened as a PNG

![mandelbrotunsmoothed](https://github.com/Tait-A/Fractals/assets/71849384/7c6a9370-964c-4b73-9ed6-2932006c4fae)


### TODO
* Create a Qt visualiser to render the fractals dynamically
* Add args to make fractal creation easier
* Compression and exporting images 