from typing import Tuple, Optional, Union
import matplotlib.pyplot as plt
import numpy as np
from mpl_toolkits.axes_grid1 import make_axes_locatable
import matplotlib.colors

from analysis_tools.plotting.plot_variables import BinningVariable
from analysis_tools.plotting.plotting_utils import (
    AxesType,
    FigureType,
    KITColors,
    set_matplotlibrc_params,
)

__all__ = [
    "Heatmap",
]


class Heatmap:
    def __init__(
        self,
        variables: Tuple[BinningVariable, BinningVariable],
        data: np.ndarray,
        limits: Optional[Tuple[np.ndarray, np.ndarray]] = None,
        z_axis_label: Optional[str] = None,
        fig_size: Tuple[float, float] = (7.0, 7.0),
        cmap: Union[str, matplotlib.colors.LinearSegmentedColormap] = "GnBu",
    ) -> None:
        self._variables = variables
        self._data = data
        self._limits = limits
        self._fig_size = fig_size
        self._z_axis_label = z_axis_label
        self._cmap = cmap

    def plot_on(
        self,
        plot_numbers: bool = False,
        plot_colorbar: bool = False,
        vmin: Optional[float] = None,
        vmax: Optional[float] = None,
        round_labels: int = 2,
        round_numbers: int = 2,
        labels_to_show: int = 1,
        upper_limit: bool = False,
        scientific_y: bool = False,
    ) -> Tuple[FigureType, AxesType]:
        set_matplotlibrc_params()
        fig, ax = plt.subplots(figsize=self.fig_size)

        im = ax.imshow(
            np.transpose(self.data),
            vmin=vmin,
            vmax=vmax,
            cmap=self.cmap,
            origin="lower",
        )

        if plot_colorbar:
            divider = make_axes_locatable(ax)
            cax = divider.append_axes("right", size="5%", pad=0.05)
            plt.colorbar(im, cax=cax)
            if self.z_axis_label:
                cax.set_ylabel(self.z_axis_label, loc="top")

        x_label, y_label = self.axes_labels()
        ax.set_xlabel(x_label, loc="right")
        ax.set_ylabel(y_label, loc="top")

        x_variable, y_variable = self.variables

        if not upper_limit:
            x_ticks = [float(x) for x in range(0, x_variable.bins)][::labels_to_show]
            x_labels = x_variable.get_bin_mids()
            y_ticks = [float(y) for y in range(0, y_variable.bins)][::labels_to_show]
            y_labels = y_variable.get_bin_mids()
        else:
            x_ticks = [x + 0.5 for x in range(-1, x_variable.bins)][::labels_to_show]
            x_labels = tuple([x_variable.get_bin_edges()[0][0]] + list(x_variable.get_upper_limits()))
            y_ticks = [y + 0.5 for y in range(-1, y_variable.bins)][::labels_to_show]
            y_labels = tuple([y_variable.get_bin_edges()[0][0]] + list(y_variable.get_upper_limits()))
        ax.set_xticks(x_ticks)
        x_axis_labels = [round(x, round_labels) if round_labels else int(round(x, round_labels)) for x in x_labels][
            ::labels_to_show
        ]
        ax.set_xticklabels(x_axis_labels)
        ax.set_yticks(y_ticks)
        y_axis_labels = [round(x, round_labels) if round_labels else int(round(x, round_labels)) for x in y_labels][
            ::labels_to_show
        ]
        if scientific_y:
            y_axis_labels = ["{:.0e}".format(x) for x in y_labels][::labels_to_show]  # type: ignore
        ax.set_yticklabels(y_axis_labels)

        if plot_numbers:
            for i in range(x_variable.bins):
                for j in range(y_variable.bins):
                    data_to_plot = self.data[i, j]
                    if not np.isnan(data_to_plot):
                        if self.limits:
                            upper_limits, lower_limits = self.limits
                            upper_uncert = round(upper_limits[i, j] - data_to_plot, round_numbers)
                            lower_uncert = round(data_to_plot - lower_limits[i, j], round_numbers)
                            text_str = r"${a}^{b}_{c}$".format(
                                a=round(data_to_plot, round_numbers),
                                b="{+" + str(upper_uncert) + "}",
                                c="{-" + str(lower_uncert) + "}",
                            )
                        else:
                            text_str = str(round(data_to_plot, round_numbers))

                        ax.text(
                            i,
                            j,
                            text_str,
                            ha="center",
                            va="center",
                            color=KITColors.kit_black,
                        )

        return fig, ax

    def axes_labels(self) -> Tuple[str, str]:
        bin_var_x, bin_var_y = self.variables
        return bin_var_x.x_label, bin_var_y.x_label

    @property
    def variables(self) -> Tuple[BinningVariable, BinningVariable]:
        return self._variables

    @property
    def data(self) -> np.ndarray:
        return self._data

    @property
    def limits(self) -> Optional[Tuple[np.ndarray, np.ndarray]]:
        return self._limits

    @property
    def z_axis_label(self) -> Optional[str]:
        return self._z_axis_label

    @property
    def fig_size(self) -> Tuple[float, float]:
        return self._fig_size

    @property
    def cmap(self) -> Union[str, matplotlib.colors.LinearSegmentedColormap]:
        return self._cmap
