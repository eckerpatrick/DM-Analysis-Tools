import os
from typing import List, Tuple, Union, Type
from cycler import cycler
import matplotlib.pyplot as plt
import matplotlib.axes._axes as axes
from matplotlib import figure

from analysis_tools.utilities.base_utils import PathType

__all__ = [
    "Unit",
    "KITColors",
    "set_matplotlibrc_params",
    "AxesType",
    "FigureType",
    "export",
]


class Unit:
    energy = r"$\mathrm{GeV}$"  # type: str
    momentum = r"$\mathrm{GeV/c}$"  # type: str
    mass = r"$\mathrm{GeV/c^2}$"  # type: str
    inv_mass = r"$\mathrm{(GeV/c^2)^{-1}}$"  # type: str

    cm = r"cm"  # type: str


class KITColors:
    """
    KIT color scheme plus additional grey shades
    """

    kit_green = "#009682"  # type: str
    kit_blue = "#4664aa"  # type: str
    kit_maygreen = "#8cb63c"  # type: str
    kit_yellow = "#fce500"  # type: str
    kit_orange = "#df9b1b"  # type: str
    kit_brown = "#a7822e"  # type: str
    kit_red = "#a22223"  # type: str
    kit_purple = "#a3107c"  # type: str
    kit_cyan = "#23a1e0"  # type: str
    kit_black = "#000000"  # type: str
    white = "#ffffff"  # type: str
    light_grey = "#bdbdbd"  # type: str
    grey = "#797979"  # type: str
    dark_grey = "#4e4e4e"  # type: str

    default_colors = [
        kit_blue,
        kit_cyan,
        kit_green,
        kit_maygreen,
        kit_red,
        kit_orange,
        kit_yellow,
        kit_purple,
        kit_brown,
        dark_grey,
    ]  # type: List[str]


kit_color_cycler = cycler("color", KITColors.default_colors)


def set_matplotlibrc_params() -> None:
    """
    Sets default parameters in the matplotlibrc.
    :return: None
    """
    xtick = {
        "top": True,
        "minor.visible": True,
        "direction": "in",
        "labelsize": 16,
    }

    ytick = {
        "right": True,
        "minor.visible": True,
        "direction": "in",
        "labelsize": 16,
    }

    axes = {
        "labelsize": 22,
        "prop_cycle": kit_color_cycler,
        "formatter.limits": (-4, 4),
        "formatter.use_mathtext": True,
        "titlesize": "large",
        "labelpad": 4.0,
    }
    lines = {
        "lw": 3.0,
        "markersize": 8,
    }
    legend = {
        "frameon": False,
        "fontsize": "large",
    }

    plt.rc("lines", **lines)
    plt.rc("axes", **axes)
    plt.rc("xtick", **xtick)
    plt.rc("ytick", **ytick)
    plt.rc("legend", **legend)

    plt.rcParams.update(
        {
            "figure.autolayout": True,
        }
    )


AxesType = Union[axes.Axes, Type[axes.Axes]]
FigureType = Union[figure.Figure, Type[figure.Figure]]


def export(
    fig: plt.Figure,
    filename: PathType,
    target_dir: PathType = "plots/",
    file_formats: Tuple[str, ...] = (".pdf", ".png"),
    close_figure: bool = True,
) -> None:
    """
    Convenience function for saving a matplotlib figure.

    :param fig: A matplotlib figure.
    :param filename: Filename of the plot without .pdf suffix.
    :param file_formats: Tuple of file formats specifying the format
                         figure will be saved as.
    :param target_dir: Directory where the plot will be saved in.
                       Default is './plots/'.
    :param close_figure: Whether to close the figure after saving it.
                         Default is False
    :return: None
    """
    os.makedirs(target_dir, exist_ok=True)

    for file_format in file_formats:
        fig.savefig(os.path.join(target_dir, f"{filename}{file_format}"), bbox_inches="tight")

    if close_figure:
        plt.close(fig)
        fig.clf()
