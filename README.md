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
style, registers several Plotly templates and sets `"jqi_nano_default"` as
the default one, and monkeypatches `pio.write_image` so every SVG export is
already cleaned up (see the Philosophy section above). Nothing else
to opt into — the rest of this README is what becomes available to you
after that one line.

One small figure helper lives outside the color/style system:
`addPlotlyLine(fig, x, y=[0, 0], clr=..., lw=2, row=None, col=None, dash=None)`
draws a straight reference line onto a Plotly figure, or a specific subplot
via `row`/`col`.

<picture><source media="(prefers-color-scheme: dark)" srcset="assets/dark/banner-colors.svg"/><img src="assets/banner-colors.svg" width="97%" alt="03 — Color Palettes and Colormaps"/></picture>

Everything below is available immediately after `from pyprettyplot import *` — no separate import.

### IBM Design Language palette

`ibm` (an instance of `IBMColors`) exposes every color in the [IBM color language](https://www.ibm.com/design/language/color) as a method taking a shade:

```python
ibm.cerulean(shade=60)   # -> "#175d8d"
ibm.red(shade=50)        # -> "#e62325"
ibm.cool_gray(shade=20)  # -> "#b8c1c1"
```

Shades run `1`–`90`, plus `100` for black and `0` for white. Available colors:
`ultramarine`, `blue`, `cerulean`, `aqua`, `teal`, `green`, `lime`, `yellow`, `gold`, `orange`, `peach`, `red`, `magenta`, `purple`, `violet`, `indigo`, `gray`, `cool_gray`, `warm_gray`, `neutral_white`, `cool_white`, `warm_white`, `black`, `white`.

Need N distinct colors instead of hand-picked shades? A few ready-made palettes are built from `ibm` already: `ibm_light_palette2`, `ibm_light_palette3`, `ibm_light_palette4`, `ibm_light_palette5`, `ibm_light_palette12`.

### Plotly templates

Registered under `pio.templates` the moment you import the package. Set one with `fig.update_layout(template="nature")`, or change the default with `pio.templates.default = "..."`.

| Template | Colorway |
|---|---|
| `"jqi_nano_default"` | **the default after import** — IBM-palette-based, the group's house style |
| `"nature"` | *Nature*-journal-style categorical colors |
| `"science"` | *Science*-journal-style categorical colors |
| `"ibm_light"` | the 12-color `ibm_light_palette12` |
| `"google"` | Google Material-style categorical colors |
| `"default"` | Plotly's own stock colorway, registered here for comparison |

`"nord"` still works too, as an alias for `"jqi_nano_default"` — kept for old code. It was the original name, but it was misleading: its colorway is the IBM palette, not the actual Nord color scheme (which sits unused elsewhere in `colors.py`). Use `"jqi_nano_default"` going forward.

Want the colors themselves rather than a whole template? `plotly_color(cycling=True, scheme="nature")` returns the `"nature"` / `"science"` / `"default"` colorway directly — a plain list (`cycling=False`) or an `itertools.cycle` (`cycling=True`).

### Scientific colormaps, via `mpl_to_plotly`

`cmcrameri` (re-exported here as `cmap`) gives you [Fabio Crameri's perceptually-uniform scientific colormaps](https://www.fabiocrameri.ch/colourmaps/) as **Matplotlib** colormap objects. With Matplotlib itself, that's already all you need — no conversion, no helper function:

```python
plt.imshow(data, cmap=cmap.acton)   # works as-is, this is plain Matplotlib
```

Plotly is the problem case: its `colorscale` argument doesn't accept a Matplotlib colormap object at all. Plotly wants its own format — a list of `[position, "rgb(r,g,b)"]` pairs, position running 0 to 1 — so a Matplotlib colormap has to be resampled into that shape before Plotly can use it. That resampling is exactly what `mpl_to_plotly(cmap.<name>, pl_entries=255, rdigits=15)` does: it walks the colormap at `pl_entries` evenly-spaced points and emits the `[position, "rgb(...)"]` list Plotly expects.

```python
fig.add_trace(go.Heatmap(z=data, colorscale=mpl_to_plotly(cmap.acton)))
```

So the rule of thumb: **Matplotlib figure → use `cmap.acton` directly; Plotly figure → wrap it, `mpl_to_plotly(cmap.acton)`.** This isn't specific to Crameri's maps either — `mpl_to_plotly` accepts any Matplotlib-style colormap object, a built-in Matplotlib map or your own `LinearSegmentedColormap` included.

A fixed subset is also pre-converted as plain module-level variables in `colors.py`, usable directly with no `mpl_to_plotly` call needed (`colorscale=acton`):

- Sequential: `acton`, `bilbao`, `davos`, `devon`, `grayC`, `lajolla`, `lapaz`, `oslo`, `tokyo`, `turku`
- Diverging: `berlin`, `broc`, `cork`, `lisbon`, `roma`, `tofino`, `vik`
- Special: `oleron` (a split, two-scale colormap)

`mpl_to_plotly` remains the general, always-correct path — reach for it by default, and treat the list above as a shortcut for just those specific maps.

### Small color helpers

- `colorFader(c1, c2, mix=0)` — linearly interpolate between two colors.
- `lighten_color(color, amount=0.5)` — lighten a single color by a given amount.

<picture><source media="(prefers-color-scheme: dark)" srcset="assets/dark/banner-defaults.svg"/><img src="assets/banner-defaults.svg" width="97%" alt="04 — Defaults"/></picture>

The Matplotlib-side defaults, loaded from the bundled `matplotlibrc` — for the Plotly-side template/colorway defaults, see Color palettes & colormaps, above.

- Axis linewidth 0.5 pt, tick linewidth 0.5 pt with a 2 pt length, no top/right spines — all in true black.
- Tick labels 6 pt, axis labels 7 pt.
- Font: **Helvetica Neue** if it's installed locally (e.g. via an Adobe Creative Cloud license), falling back to matplotlib's default sans-serif otherwise. No font files are bundled in this package — see
  [ScientificGraphicDesign/04-Fonts](https://github.com/JQInanophotonics/ScientificGraphicDesign/tree/main/04-Fonts)
  for why and how to install it.

<picture><source media="(prefers-color-scheme: dark)" srcset="assets/dark/banner-whats-in-here.svg"/><img src="assets/banner-whats-in-here.svg" width="97%" alt="05 — What's in Here"/></picture>

```
pyprettyplot/
├── setup.py
├── requirements.txt
└── pyprettyplot/
    ├── requirements.txt   — same pinned dependencies, kept alongside the package data
    ├── __init__.py        — plotly helpers, style setup, SVG/figure export
    ├── colors.py          — color palettes and colormaps (IBM, Crameri, SecretColors wrappers)
    ├── gregplot.py        — additional matplotlib plotting helpers (not auto-imported)
    └── matplotlibrc       — the matplotlib style sheet this package loads by default
```

<picture><source media="(prefers-color-scheme: dark)" srcset="assets/dark/banner-see-also.svg"/><img src="assets/banner-see-also.svg" width="97%" alt="06 — See Also"/></picture>

Part of the [JQInanophotonics](https://github.com/JQInanophotonics) org. Start with
[ScientificGraphicDesign](https://github.com/JQInanophotonics/ScientificGraphicDesign)
for the group's broader guide to making publication-quality figures.
