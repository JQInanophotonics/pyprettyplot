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

## Philosophy

Most of what makes a figure look "publication-ready" is mechanical, not
creative — the same handful of style decisions applied consistently across
every plot. So `pyprettyplot` automates that part instead of leaving it to
be fixed by hand in Illustrator every time:

- **Style defaults out of the box.** Import it and your plots already look
  like a Nature-style figure: only the left and bottom spines are drawn (no
  box), thin consistent line/tick widths, true black instead of default
  Matplotlib gray, and the group's standard font sizes. You're not starting
  from Matplotlib's defaults and manually stripping spines/gridlines/box on
  every figure.
- **The export itself is patched, not just the style.** `pio.write_image`
  (from Plotly) normally leaves a fair amount of junk in an exported SVG:
  a background rect you don't want, the left and bottom axis spines drawn
  as two disconnected path segments instead of one continuous line, and
  tick marks that don't sit exactly on the spine coordinate (visible the
  moment you zoom in in a vector editor). `pyprettyplot.write_image` wraps
  Plotly's exporter and post-processes the SVG to fix exactly this: it
  drops the background rect, merges the two spine segments into a single
  path, and snaps every tick mark onto the true spine position. What you
  get out is a clean SVG you can drop straight into Illustrator without
  first cleaning up after the renderer.

The specific values (spine widths, font sizes, colors) come from the
group's house style — see the "rules, in one screen" section of
[ScientificGraphicDesign](https://github.com/JQInanophotonics/ScientificGraphicDesign)
for the reasoning behind them.

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
