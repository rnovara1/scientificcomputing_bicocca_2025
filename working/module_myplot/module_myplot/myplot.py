"""
Decorator for matplotlib plots to apply consistent style and
optionally add grids and save the figure to a pdf file.
"""

from matplotlib import rc
import matplotlib.pyplot as plt
import matplotlib
from matplotlib.ticker import LogLocator

import functools
import os

def myplot(func):

    @functools.wraps(func)
    def wrapper(*args, save=True, filename=None, dpi=300, path=".", grid=True, **kwargs):

        # --- Global style settings ---
        font = {
            'family': 'serif',
            'serif': ['cmr10'],
            'weight': 'medium',
            'size': 16
        }
        rc('font', **font)
        rc('text', usetex=True)
        matplotlib.rcParams['text.latex.preamble'] = r"\usepackage{amsmath}"
        matplotlib.rcParams["axes.formatter.use_mathtext"] = True

        rc('figure', max_open_warning=1000)
        rc('ytick', right=False, labelsize=14)
        rc('xtick', top=False, labelsize=14)
        rc("axes", grid=False, titlesize=18, labelsize=16)

        # --- Call original plotting function ---
        fig = func(*args, **kwargs)

        # --- Layout ---
        if hasattr(fig, "set_constrained_layout"):
            fig.set_constrained_layout(True)

        # --- Add grid only if requested ---
        if grid:
            for ax in fig.axes:
                ax.set_axisbelow(True)  # grid behind lines
                # Major grid
                ax.grid(True, which='major', linestyle='--', linewidth=0.5, alpha=0.6)
                # Minor grid
                ax.grid(True, which='minor', linestyle=':', linewidth=0.5, alpha=0.4)

        # --- Add minor ticks for log scales regardless of grid ---
        for ax in fig.axes:
            if ax.get_xscale() == 'log':
                ax.xaxis.set_minor_locator(LogLocator(base=10.0, subs=None, numticks=10))
            if ax.get_yscale() == 'log':
                ax.yaxis.set_minor_locator(LogLocator(base=10.0, subs=None, numticks=10))

        # --- Save figure ---
        if save:
            if not os.path.exists(path):
                os.makedirs(path)

            # Auto-name file after function name if user does not specify
            if filename is None:
                filename = f"{func.__name__}.pdf"
            else:
                filename = os.path.splitext(filename)[0] + ".pdf"

            filepath = os.path.join(path, filename)
            fig.savefig(filepath, dpi=dpi, bbox_inches="tight")

            print(f"[myplot] Figure saved to: {filepath}")

        plt.show()

        plt.close(fig)

    return wrapper
