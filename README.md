<div align="center">

<picture><source media="(prefers-color-scheme: dark)" srcset="assets/dark/header.svg"/><img src="assets/header.svg" width="97%" alt="pyprettyplot"/></picture>

<a href="#install"><picture><source media="(prefers-color-scheme: dark)" srcset="https://img.shields.io/badge/INSTALL-0d1117?style=flat-square&logoColor=ffffff"/><img src="https://img.shields.io/badge/INSTALL-ffffff?style=flat-square&logoColor=1a1a1a" alt="Install"/></picture></a>
<a href="https://github.com/JQInanophotonics/ScientificGraphicDesign"><picture><source media="(prefers-color-scheme: dark)" srcset="https://img.shields.io/badge/GRAPHIC%20DESIGN-0d1117?style=flat-square&logoColor=ffffff"/><img src="https://img.shields.io/badge/GRAPHIC%20DESIGN-ffffff?style=flat-square&logoColor=1a1a1a" alt="ScientificGraphicDesign"/></picture></a>
<a href="https://github.com/JQInanophotonics/ScientificGraphicDesign/tree/main/01-Plotting"><picture><source media="(prefers-color-scheme: dark)" srcset="https://img.shields.io/badge/PLOTTING%20EXAMPLE-0d1117?style=flat-square&logoColor=ffffff"/><img src="https://img.shields.io/badge/PLOTTING%20EXAMPLE-ffffff?style=flat-square&logoColor=1a1a1a" alt="Plotting example"/></picture></a>

</div>

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

<picture><source media="(prefers-color-scheme: dark)" srcset="assets/dark/banner-philosophy.svg"/><img src="assets/banner-philosophy.svg" width="97%" alt="00 — Philosophy"/></picture>

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

<picture><source media="(prefers-color-scheme: dark)" srcset="assets/dark/banner-install.svg"/><img src="assets/banner-install.svg" width="97%" alt="01 — Install"/></picture>

```
pip install git+https://github.com/JQInanophotonics/pyprettyplot.git
```

Or, for a local/editable install (e.g. if you want to read or modify the source):

```
git clone https://github.com/JQInanophotonics/pyprettyplot.git
cd pyprettyplot
pip install -r requirements.txt
pip install -e .
```

<picture><source media="(prefers-color-scheme: dark)" srcset="assets/dark/banner-use.svg"/><img src="assets/banner-use.svg" width="97%" alt="02 — Use"/></picture>

```python
from pyprettyplot import *
```

This one import does everything at once: loads the group's `matplotlibrc`
style, registers several Plotly templates and sets `"nord"` as the default
one, and monkeypatches `pio.write_image` so every SVG export is
already cleaned up (see the Philosophy section above). Nothing else
to opt into — the rest of this README is what becomes available to you
after that one line.

<picture><source media="(prefers-color-scheme: dark)" srcset="assets/dark/banner-colors.svg"/><img src="assets/banner-colors.svg" width="97%" alt="03 — Color Palettes and Colormaps"/></picture>

Everything below is available immediately after `from pyprettyplot import *` — no separate import.

**IBM Design Language palette.** `ibm` (an instance of `IBMColors`) exposes every color in the [IBM color language](https://www.ibm.com/design/language/color) as a method taking a shade (`1`–`90`, plus `100` for black and `0` for white):

```python
ibm.cerulean(shade=60)   # -> "#175d8d"
ibm.red(shade=50)        # -> "#e62325"
ibm.cool_gray(shade=20)  # -> "#b8c1c1"
```

Available colors: `ultramarine`, `blue`, `cerulean`, `aqua`, `teal`, `green`, `lime`, `yellow`, `gold`, `orange`, `peach`, `red`, `magenta`, `purple`, `violet`, `indigo`, `gray`, `cool_gray`, `warm_gray`, `neutral_white`, `cool_white`, `warm_white`, `black`, `white`.

For when you just need N distinct colors rather than hand-picked shades, a few categorical palettes built from `ibm` are ready to use: `ibm_light_palette2`, `ibm_light_palette3`, `ibm_light_palette4`, `ibm_light_palette5`, `ibm_light_palette12`.

**Plotly templates**, registered under `pio.templates` the moment you import the package — set one with `fig.update_layout(template="nature")`, or change the default with `pio.templates.default = "..."`:

| Template | Colorway |
|---|---|
| `"nord"` | **the default after import** — IBM-palette-based, matches the group's house style |
| `"nature"` | *Nature*-journal-style categorical colors |
| `"science"` | *Science*-journal-style categorical colors |
| `"ibm_light"` | the 12-color `ibm_light_palette12` |
| `"google"` | Google Material-style categorical colors |
| `"default"` | Plotly's own stock colorway, registered here for comparison |

`plotly_color(cycling=True, scheme="nature")` returns the same `"nature"` / `"science"` / `"default"` colorways directly — as a plain list (`cycling=False`) or as an `itertools.cycle` (`cycling=True`), for when you want the colors themselves rather than a whole template.

**Scientific colormaps, pre-converted for Plotly.** [Fabio Crameri's perceptually-uniform scientific colormaps](https://www.fabiocrameri.ch/colourmaps/) are already converted to Plotly's `colorscale` format and importable by name — no conversion step needed:

- Sequential: `acton`, `bilbao`, `davos`, `devon`, `grayC`, `lajolla`, `lapaz`, `oslo`, `tokyo`, `turku`
- Diverging: `berlin`, `broc`, `cork`, `lisbon`, `roma`, `tofino`, `vik`
- Special: `oleron` (a split, two-scale colormap)

```python
fig.add_trace(go.Heatmap(z=data, colorscale=acton))
```

For any other colormap — a different `cmcrameri` map, a Matplotlib built-in, or your own `LinearSegmentedColormap` — convert it yourself with `mpl_to_plotly(cmap, pl_entries=255, rdigits=15)`, the same function the colormaps above were generated with.

Two small color-math helpers round this out: `colorFader(c1, c2, mix=0)` linearly interpolates between two colors, and `lighten_color(color, amount=0.5)` lightens a single color by a given amount.

<picture><source media="(prefers-color-scheme: dark)" srcset="assets/dark/banner-helpers.svg"/><img src="assets/banner-helpers.svg" width="97%" alt="04 — Other Helpers"/></picture>

- `addPlotlyLine(fig, x, y=[0, 0], clr=..., lw=2, row=None, col=None, dash=None)` — draw a straight reference line onto a Plotly figure, or a specific subplot via `row`/`col`.
- `loadOSA(fname, noise=-85, freq_lim=[None, None])` — load an optical spectrum analyzer CSV export into a tidy `freq`/`lbd`/`S` dataframe, clipping the noise floor and optionally restricting to a frequency range.
- Dispersion/coupling post-processing (`dispersion.py`, also auto-imported): `getDisp`, `getDint`, `getδf`, `getSFG`, `ProcessDispSim`, `ProcessCoupling` — turn microresonator simulation output (mode number, frequency, geometry sweeps) into effective index, group index, integrated dispersion (`Dint`), FSR, and related quantities. Specific to this group's photonics simulations, not general-purpose plotting.

**Not auto-imported:** `gregplot.py` also ships in this package (matplotlib helpers, a `createColor` gradient function, spine/font adjustment) but its import is commented out in `__init__.py` — `from pyprettyplot import *` will not give you these. Use `from pyprettyplot.gregplot import <name>` explicitly if you need them.

<picture><source media="(prefers-color-scheme: dark)" srcset="assets/dark/banner-defaults.svg"/><img src="assets/banner-defaults.svg" width="97%" alt="05 — Defaults"/></picture>

The Matplotlib-side defaults, loaded from the bundled `matplotlibrc` — for the Plotly-side template/colorway defaults, see Color palettes & colormaps, above.

- Axis linewidth 0.5 pt, tick linewidth 0.5 pt with a 2 pt length, no top/right spines — all in true black.
- Tick labels 6 pt, axis labels 7 pt.
- Font: **Helvetica Neue** if it's installed locally (e.g. via an Adobe Creative Cloud license), falling back to matplotlib's default sans-serif otherwise. No font files are bundled in this package — see
  [ScientificGraphicDesign/04-Fonts](https://github.com/JQInanophotonics/ScientificGraphicDesign/tree/main/04-Fonts)
  for why and how to install it.

<picture><source media="(prefers-color-scheme: dark)" srcset="assets/dark/banner-whats-in-here.svg"/><img src="assets/banner-whats-in-here.svg" width="97%" alt="06 — What's in Here"/></picture>

```
pyprettyplot/
├── setup.py
├── requirements.txt
└── pyprettyplot/
    ├── requirements.txt   — same pinned dependencies, kept alongside the package data
    ├── __init__.py        — plotly helpers, style setup, SVG/figure export
    ├── colors.py          — color palettes and colormaps (IBM, Nord, Crameri, SecretColors wrappers)
    ├── dispersion.py      — microresonator dispersion/coupling processing helpers
    ├── gregplot.py        — additional matplotlib plotting helpers (not auto-imported)
    └── matplotlibrc       — the matplotlib style sheet this package loads by default
```

<picture><source media="(prefers-color-scheme: dark)" srcset="assets/dark/banner-see-also.svg"/><img src="assets/banner-see-also.svg" width="97%" alt="07 — See Also"/></picture>

Part of the [JQInanophotonics](https://github.com/JQInanophotonics) org. Start with
[ScientificGraphicDesign](https://github.com/JQInanophotonics/ScientificGraphicDesign)
for the group's broader guide to making publication-quality figures.
