## TAIT-A's Fractals

### A repository for visualising mandelbrot and julia sets

#### Prerequisites

To run install pixi: https://pixi.sh/dev/
Then run ```pixi install``` from the root dir.

#### Running

```pixi run julia```

This will generate a random Julia set, to specify the complex number use the args '--real' and '--imag':
```pixi run julia --real 0.28 --image 0.008```

or 
```pixi run mandelbrot```
This will generate the mandelbrot set.


The colour gradient can be set using the flag ```--colour```, this works for both julia and mandelbrot sets.

The output will be opened as a PNG



### TODO
* Create a Qt visualiser to render the fractals dynamically
* Add args to make fractal creation easier
* Compression and exporting images 