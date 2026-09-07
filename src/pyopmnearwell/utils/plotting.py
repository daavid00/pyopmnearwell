"""Save pyopmnearwell figures and the data needed to reproduce them."""

import pathlib
import pickle

import matplotlib.pyplot as plt
from matplotlib.figure import Figure


def save_fig_and_data(fig: Figure, path: str | pathlib.Path) -> None:
    """Save a figure and its plotting data.

    The figure is written as an SVG file and the complete Matplotlib figure object
    is serialized to a Pickle file with the same stem. The input figure is closed
    after both files have been written.

    Parameters
    ----------
    fig : matplotlib.figure.Figure
        Figure to save and serialize.
    path : str | pathlib.Path
        Output path. Existing suffixes are replaced by ``.svg`` and ``.pickle``.
    """
    # Convert to a path in case a string was passed.
    path = pathlib.Path(path)

    # Save the figure to a png file
    # NOTE: Convert filename to str to ensure this works. With fig, ax = plt.subplots()
    # the conversion is not necessary, but with fig = plt.figure() it is.
    fig.savefig(
        str(path.with_suffix(".svg")), bbox_inches="tight", format="svg", dpi=300
    )

    # Save the data to a pickle file
    with path.with_suffix(".pickle").open("wb") as f:  # pylint: disable=C0103
        pickle.dump(fig, f)

    plt.close(fig)
