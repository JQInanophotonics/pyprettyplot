# pyprettyplot

A small Python package that pre-loads a consistent plotting style — for
[`matplotlib`](https://matplotlib.org/) and
[`plotly`](https://plotly.com/python/) alike — so figures look the same
whether they're made during an experiment or for a paper. Used across the
Srinivasan Group at JQI; see
[ScientificGraphicDesign](https://github.com/JQInanophotonics/ScientificGraphicDesign)
for the broader house style this package implements, and
[01 — Plotting data](https://github.com/JQInanophotonics/ScientificGraphicDesign/tree/main/01-Plotting)
for a worked example.

This package used to live inside `ScientificGraphicDesign` directly; it's
now its own repo so it can be installed and versioned independently of
those tutorials.

## Install

```
pip install git+https://github.com/JQInanophotonics/pyprettyplot.git
```

## Use

```python
from pyprettyplot import *
```

## Defaults

- Axis linewidth 0.5 pt, tick linewidth 0.5 pt with a 2 pt length, no top/right spines — all in true black.
- Tick labels 6 pt, axis labels 7 pt.
- Font: **Helvetica Neue** if it's installed locally (e.g. via an Adobe Creative Cloud license), falling back to matplotlib's default sans-serif otherwise. No font files are bundled in this package — see
  [ScientificGraphicDesign/04-Fonts](https://github.com/JQInanophotonics/ScientificGraphicDesign/tree/main/04-Fonts)
  for why and how to install it.
- Cycling color palette based on the [Nord theme](https://www.nordtheme.com/docs/colors-and-palettes).
- `colors.py` also exposes an `IBMColors` class (instantiated as `ibm`) for the [IBM color palette](https://www.ibm.com/design/language/color), e.g. `ibm.cerulean(shade=60)`.

## What's in here

```
pyprettyplot/
├── setup.py
├── requirements.txt (via pyprettyplot/requirements.txt)
└── pyprettyplot/
    ├── __init__.py       — plotly helpers, style setup, SVG/figure export
    ├── colors.py         — color palettes and colormaps (IBM, Nord, SecretColors wrappers)
    ├── dispersion.py     — microresonator dispersion/coupling processing helpers
    ├── gregplot.py       — additional matplotlib plotting helpers
    └── matplotlibrc      — the matplotlib style sheet this package loads by default
```

## See also

Part of the [JQInanophotonics](https://github.com/JQInanophotonics) org. Start with
[ScientificGraphicDesign](https://github.com/JQInanophotonics/ScientificGraphicDesign)
for the group's broader guide to making publication-quality figures.
