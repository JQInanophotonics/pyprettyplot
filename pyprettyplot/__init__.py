import sys
import os
import re

import pickle as pkl
import numpy as np
from scipy import signal
from glob import glob

import matplotlib as mpl
import plotly.graph_objs as go
import plotly.io as pio
from plotly.subplots import make_subplots
import plotly.graph_objects as go

pio.templates.default = "plotly_white"
from matplotlib.colors import LinearSegmentedColormap, to_hex
from itertools import cycle
import warnings

warnings.filterwarnings("ignore")

zclr = "#B1BDDA"

from matplotlib import pyplot as plt
import matplotlib.font_manager as fm
file_path = os.path.dirname(__file__)
rcFile = f"{file_path}/matplotlibrc"
mpl.rcParams.update(mpl.rc_params_from_file(rcFile))

# Helvetica Neue is licensed separately (Adobe CC) and not bundled here;
# fall back to matplotlib's default sans-serif if it isn't installed locally.
try:
    fm.findfont("Helvetica Neue", fallback_to_default=False)
    label_font = fm.FontProperties(family="Helvetica Neue")
except ValueError:
    label_font = fm.FontProperties(family="sans-serif")
label = dict(fontproperties=label_font, fontsize=8)
px = 1/plt.rcParams['figure.dpi']

def addPlotlyLine(fig, x, y=[0, 0], clr=zclr, lw=2, row=None, col=None, dash=None):
    if row == None and col == None:
        fig.add_shape(
            type="line",
            x0=x[0],
            x1=x[1],
            y0=y[0],
            y1=y[1],
            line=dict(color=clr, width=lw, dash=dash),
        )
    else:
        fig.add_shape(
            type="line",
            x0=x[0],
            x1=x[1],
            y0=y[0],
            y1=y[1],
            line=dict(color=clr, width=lw, dash=dash),
            row=row,
            col=col,
        )

from .colors import *
# from .gregplot import *
# from .lineardata import *
# from .plotlyServer import plotlyServer

pio.templates.default = "jqi_nano_default"


# Fixes applied at export time. Everything that renders (show, write_image,
# write_html, to_json) goes through to_dict().
#
# plotly.js draws 10^n tick labels 1.25x bigger on log axes with
# exponentformat='power' (hardcoded in axes.js); undo it so the labels come out
# at the tickfont size actually requested.
_POWER_LOG_SCALE = 1.25
# Take the originals from plotly itself, not from go.Figure / pio, so that
# re-running this module (%autoreload) doesn't wrap the patch around itself.
from plotly.basedatatypes import BaseFigure

_plotly_to_dict = BaseFigure.to_dict


def _axis_attr(name, layout, tmpl_layout, *path):
    tmpl_ax = tmpl_layout.get(re.sub(r"\d+$", "", name), {})
    for src in (layout[name], tmpl_ax):
        for key in path:
            src = src.get(key) if isinstance(src, dict) else None
        if src is not None:
            return src
    return None


def _merge(base, override):
    out = dict(base)
    for k, v in override.items():
        out[k] = _merge(out[k], v) if isinstance(v, dict) and isinstance(out.get(k), dict) else v
    return out


def _export_fixes(self, *args, **kwargs):
    fig = _plotly_to_dict(self, *args, **kwargs)
    layout = fig.get("layout", {})
    tmpl_layout = layout.get("template", {}).get("layout", {})

    # Templates only style `legend`; legend2, legend3, ... would fall back to
    # plotly defaults, so give them the template legend style too (the figure's
    # own legendN settings still win).
    tmpl_legend = tmpl_layout.get("legend", {})
    legends = {t.get("legend") for t in fig.get("data", [])}
    legends |= {k for k in layout if re.fullmatch(r"legend\d+", k)}
    for name in legends - {None, "legend"}:
        layout[name] = _merge(tmpl_legend, layout.get(name, {}))

    for name in [k for k in layout if re.fullmatch(r"[xy]axis\d*", k)]:
        if _axis_attr(name, layout, tmpl_layout, "type") != "log":
            continue
        if _axis_attr(name, layout, tmpl_layout, "exponentformat") != "power":
            continue
        fsize = (
            _axis_attr(name, layout, tmpl_layout, "tickfont", "size")
            or layout.get("font", {}).get("size")
            or tmpl_layout.get("font", {}).get("size")
            or 12
        )
        layout[name].setdefault("tickfont", {})["size"] = fsize / _POWER_LOG_SCALE
    return fig


go.Figure.to_dict = _export_fixes





import plotly.io as pio
from lxml import etree
import re

from plotly.io._kaleido import write_image as _original_write_image

def _fix_svg_corners(svg_bytes):
    root = etree.fromstring(svg_bytes)
    ns = 'http://www.w3.org/2000/svg'

    # Remove background rect
    for rect in root.findall(f'{{{ns}}}rect'):
        root.remove(rect)

    # Process each subplot group independently
    for g in root.findall(f'.//{{{ns}}}g'):
        cls = g.get('class') or ''
        if not re.match(r'subplot ', cls):
            continue

        # Get spine paths within this subplot group
        xline = next((c for c in g if 'xlines-above' in (c.get('class') or '')), None)
        yline = next((c for c in g if 'ylines-above' in (c.get('class') or '')), None)
        if xline is None or yline is None:
            continue

        xd = xline.get('d', '').strip()
        yd = yline.get('d', '').strip()
        if not xd or not yd:
            continue

        xm = re.match(r'M\s*([\d.]+),([\d.]+)\s*H\s*([\d.]+)', xd)
        ym = re.match(r'M\s*([\d.]+),([\d.]+)\s*V\s*([\d.]+)', yd)
        if not xm or not ym:
            continue

        x_spine = float(ym.group(1))
        y_spine = float(xm.group(2))
        x2 = xm.group(3)
        y1 = ym.group(2)

        # Merge into single L-path and clear yline
        xline.set('d', f"M{x_spine},{y1}V{y_spine}H{x2}")
        yline.set('d', '')

        # Get linewidth
        style = xline.get('style', '')
        lw_match = re.search(r'stroke-width:\s*([\d.]+)px', style)
        lw = float(lw_match.group(1)) if lw_match else 1.0

        # Fix xticks within xaxislayer-above of this subplot
        xaxislayer = next((c for c in g if 'xaxislayer-above' in (c.get('class') or '')), None)
        if xaxislayer is not None:
            for tick in xaxislayer.findall(f'.//{{{ns}}}path'):
                if 'ticks' not in (tick.get('class') or ''):
                    continue
                td = tick.get('d', '')
                tm = re.match(r'M([\d.-]+),([\d.-]+)(v[\d.-]+)', td)
                if tm:
                    tick.set('d', f"M{tm.group(1)},{y_spine}{tm.group(3)}")
                tick_style = tick.get('style', '')
                if 'fill' not in tick_style:
                    tick.set('style', tick_style + '; fill: none;')

        # Fix yticks within yaxislayer-above of this subplot
        yaxislayer = next((c for c in g if 'yaxislayer-above' in (c.get('class') or '')), None)
        if yaxislayer is not None:
            for tick in yaxislayer.findall(f'.//{{{ns}}}path'):
                if 'ticks' not in (tick.get('class') or ''):
                    continue
                td = tick.get('d', '')
                tm = re.match(r'M([\d.-]+),([\d.-]+)(h[\d.-]+)', td)
                if tm:
                    tick.set('d', f"M{x_spine},{tm.group(2)}{tm.group(3)}")
                tick_style = tick.get('style', '')
                if 'fill' not in tick_style:
                    tick.set('style', tick_style + '; fill: none;')

    return etree.tostring(root)

def write_image(fig, file, **kwargs):
    if str(file).endswith('.svg'):
        svg_bytes = pio.to_image(fig, format='svg', **kwargs)
        fixed = _fix_svg_corners(svg_bytes)
        with open(file, 'wb') as f:
            f.write(fixed)
    else:
        _original_write_image(fig, file, **kwargs)

pio.write_image = write_image


