# uchimata-py

This repository contains code for the Python widget version of the
[uchimata](https://github.com/dvdkouril/uchimata) library. Made with
[anywidget](https://github.com/manzt/anywidget), this allows people to use the
functionality in computational notebooks, such as Jupyter Notebook.

![colorful squiggly thick line depicting 3D chromatin running in jupyter
notebook](./spyce-teaser.gif)

## Basic usage
The available functionality is pretty limited at this moment. We will stabilize
the API as we go. At this point, you can display 3D chromatin models.

```python
import uchimata as uchi
import numpy as np

BINS_NUM = 1000

# Step 1: Generate random structure, returns a 2D numpy array:
def make_random_3D_chromatin_structure(n):
    position = np.array([0.0, 0.0, 0.0])
    positions = [position.copy()]
    for _ in range(n):
        step = np.random.choice([-1.0, 0.0, 1.0], size=3)  # Randomly choose to move left, right, up, down, forward, or backward
        position += step
        positions.append(position.copy())
    return np.array(positions)

random_structure = make_random_3D_chromatin_structure(BINS_NUM)

# Step 2: Display the structure in an uchimata widget
numbers = list(range(0, BINS_NUM+1))
vc = {
    "color": {
        "values": numbers,
        "min": 0,
        "max": BINS_NUM,
        "colorScale": "Spectral"
    }, 
    "scale": 0.01, 
    "links": True, 
    "mark": "sphere"
}
uchi.Widget(random_structure, vc)
```

The underlying JS library [only supports data in the Apache Arrow
format](https://github.com/dvdkouril/uchimata/tree/main/docs#data-loading).

In the widget version, on the other hand, we provide interface to load data in
many notebook-native formats, such as 2D numpy arrays, or pandas dataframe
(with columns named `'x'`, `'y'`, `'z'`).

Quickly test out **uchimata** with [uv](https://docs.astral.sh/uv/):
1. `uv run --with uchimata --with numpy --with pyarrow --with jupyterlab
   jupyter lab`
2. make a new notebook
3. copy and paste the code above into an empty cell

Or: [run the example in Google
Colab](https://colab.research.google.com/drive/1EZh9HcGS3cgPF4C6eFyMm5iHGVGS4Cj_?usp=sharing).

## Contributing
Running tests:
`uv run pytest`
