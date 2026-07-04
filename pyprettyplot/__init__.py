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





import plotly.io as pio
from lxml import etree
import re

_original_write_image = pio.write_image

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


