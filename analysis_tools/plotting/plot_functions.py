import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from typing import Tuple, Optional

from analysis_tools.plotting.plot_variables import BinningVariable, HistVariable
from analysis_tools.plotting.plotting_utils import AxesType, FigureType, set_matplotlibrc_params
from analysis_tools.plotting.heatmap import Heatmap

__all__ = [
    "plot_2d_fractions",
    "plot_2d_numbers",
    "plot_scatter",
]


def plot_2d_fractions(
    df: pd.DataFrame,
    binning_variables: Tuple[BinningVariable, BinningVariable],
    weight_column: Optional[str] = None,
    plot_numbers: bool = True,
    labels_to_show: int = 1,
    round_labels: bool = False,
    round_numbers: int = 2,
) -> Tuple[FigureType, AxesType]:
    binning_var_1, binning_var_2 = binning_variables
    fractions = np.full(
        (binning_var_1.bins, binning_var_2.bins),
        fill_value=np.nan,
    )

    for i, first_limits in enumerate(binning_var_1.get_bin_edges()):
        first_lower, first_upper = first_limits
        for j, second_limits in enumerate(binning_var_2.get_bin_edges()):
            sec_lower, sec_upper = second_limits
            first_lower_cond = df[binning_var_1.df_label] >= first_lower
            first_upper_cond = df[binning_var_1.df_label] < first_upper
            if i == len(binning_var_1.get_bin_edges()) - 1:
                first_upper_cond = df[binning_var_1.df_label] <= first_upper
            sec_lower_cond = df[binning_var_2.df_label] >= sec_lower
            sec_upper_cond = df[binning_var_2.df_label] < sec_upper
            if j == len(binning_var_2.get_bin_edges()) - 1:
                sec_upper_cond = df[binning_var_2.df_label] <= sec_upper

            df_bin = df.loc[first_lower_cond & first_upper_cond & sec_lower_cond & sec_upper_cond]
            if len(df) > 0:
                if not weight_column:
                    fraction = len(df_bin) / len(df)
                else:
                    fraction = np.sum(df_bin[weight_column]) / np.sum(df[weight_column])
            else:
                fraction = 0
            fractions[i][j] = fraction

    hp = Heatmap(
        variables=(binning_var_1, binning_var_2),
        data=fractions,
        z_axis_label="Fraction",
    )
    fig, ax = hp.plot_on(
        plot_numbers=plot_numbers,
        plot_colorbar=True,
        vmin=0,
        upper_limit=True,
        labels_to_show=labels_to_show,
        round_labels=round_labels,
        round_numbers=round_numbers,
    )

    return fig, ax


def plot_2d_numbers(
    df: pd.DataFrame,
    binning_variables: Tuple[BinningVariable, BinningVariable],
    weight_column: Optional[str] = None,
) -> Tuple[FigureType, AxesType]:
    binning_var_1, binning_var_2 = binning_variables
    numbers = np.full(
        (binning_var_1.bins, binning_var_2.bins),
        fill_value=np.nan,
    )

    for i, first_limits in enumerate(binning_var_1.get_bin_edges()):
        first_lower, first_upper = first_limits
        for j, second_limits in enumerate(binning_var_2.get_bin_edges()):
            sec_lower, sec_upper = second_limits
            first_lower_cond = df[binning_var_1.df_label] >= first_lower
            first_upper_cond = df[binning_var_1.df_label] < first_upper
            if i == len(binning_var_1.get_bin_edges()) - 1:
                first_upper_cond = df[binning_var_1.df_label] <= first_upper
            sec_lower_cond = df[binning_var_2.df_label] >= sec_lower
            sec_upper_cond = df[binning_var_2.df_label] < sec_upper
            if j == len(binning_var_2.get_bin_edges()) - 1:
                sec_upper_cond = df[binning_var_2.df_label] <= sec_upper

            df_bin = df.loc[first_lower_cond & first_upper_cond & sec_lower_cond & sec_upper_cond]
            if len(df) > 0:
                if not weight_column:
                    number = len(df_bin)
                else:
                    number = np.sum(df_bin[weight_column])
            else:
                number = 0
            numbers[i][j] = number

    hp = Heatmap(
        variables=(binning_var_1, binning_var_2),
        data=numbers,
        z_axis_label="N",
    )
    fig, ax = hp.plot_on(
        plot_numbers=False,
        plot_colorbar=True,
        vmin=0,
        upper_limit=True,
    )

    return fig, ax


def plot_scatter(
    df: pd.DataFrame,
    hist_variables: Tuple[HistVariable, HistVariable],
    color: Optional[str] = None,
    label: Optional[str] = None,
    fig: Optional[FigureType] = None,
    ax: Optional[AxesType] = None,
    s: float = 0.05,
) -> Tuple[FigureType, AxesType]:
    set_matplotlibrc_params()

    hist_variable_x, hist_variable_y = hist_variables

    if fig is None:
        assert ax is None
        fig, ax = plt.subplots()

    assert ax is not None
    ax.scatter(
        df[hist_variable_x.df_label],
        df[hist_variable_y.df_label],
        marker="D",
        color=color,
        label=label,
        s=s,
        lw=1,
    )

    if hist_variable_x.scope:
        ax.set_xlim(hist_variable_x.scope)
    if hist_variable_y.scope:
        ax.set_ylim(hist_variable_y.scope)

    ax.set_xlabel(hist_variable_x.x_label, loc="right")
    ax.set_ylabel(hist_variable_y.x_label, loc="top")

    return fig, ax
