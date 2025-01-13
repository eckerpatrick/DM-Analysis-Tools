import matplotlib.pyplot as plt
import numpy as np
from typing import Optional, Union, Tuple
import pandas as pd
from enum import Enum

from analysis_tools.plotting.plot_variables import HistVariable
from analysis_tools.plotting.histogram_component import HistogramComponent
from analysis_tools.plotting.histogram import Histogram
from analysis_tools.plotting.plotting_utils import (
    AxesType,
    FigureType,
    KITColors,
    set_matplotlibrc_params,
)

__all__ = [
    "HistogramPlot",
]


class HistogramPlotType(Enum):
    candidates = "Candidates"
    events = "Events"


class HistogramPlot:
    def __init__(
        self,
        hist_var: HistVariable,
        title: Optional[str] = None,
        stacked: bool = True,
        hist_type: str = "stepfilled",
        normed: bool = False,
        uncertainty: bool = True,
        y_log: bool = False,
        luminosity: Optional[float] = None,
        additional_lumi_text: str = None,
        fig_size: Tuple[float, float] = (8.0, 6.0),
        histogram_plot_type: HistogramPlotType = HistogramPlotType.candidates,
    ) -> None:
        self._hist_var = hist_var
        self._title = title
        self._stacked = stacked
        self._hist_type = hist_type
        self._normed = normed
        self._uncertainty = uncertainty
        self._y_log = y_log
        self._luminosity = luminosity
        self._additional_lumi_text = additional_lumi_text
        self._fig_size = fig_size
        self._histogram_plot_type = histogram_plot_type

        self._histogram = Histogram(variable=self.hist_var)

    def prepare_data_and_weights(
        self,
        data: Union[pd.DataFrame, pd.Series, np.ndarray],
        weights: Optional[Union[str, pd.Series, np.ndarray]] = None,
    ) -> Tuple[np.ndarray, Optional[np.ndarray]]:
        if isinstance(data, pd.DataFrame):
            hist_data = np.array(data[self.hist_var.df_label])
        elif isinstance(data, pd.Series):
            hist_data = np.array(data)
        elif isinstance(data, np.ndarray):
            hist_data = data
        else:
            raise ValueError

        if weights is not None:
            if isinstance(weights, str):
                assert isinstance(data, pd.DataFrame)
                hist_weights = np.array(data[weights])  # type: Optional[np.ndarray]
            elif isinstance(weights, pd.Series):
                hist_weights = np.array(weights)
            elif isinstance(weights, np.ndarray):
                hist_weights = weights
            else:
                raise ValueError
        else:
            hist_weights = None

        return hist_data, hist_weights

    def add_component(
        self,
        data: Union[pd.DataFrame, pd.Series, np.ndarray],
        label: str,
        weights: Optional[Union[str, pd.Series, np.ndarray]] = None,
        color: Optional[str] = None,
    ) -> None:
        hist_data, hist_weights = self.prepare_data_and_weights(data=data, weights=weights)
        hist_component = HistogramComponent(
            data=hist_data,
            label=label,
            weights=hist_weights,
            color=color,
        )
        self._histogram.add_component(hist_component=hist_component)

    def add_signal_component(
        self,
        data: Union[pd.DataFrame, pd.Series, np.ndarray],
        label: str,
        weights: Optional[Union[str, pd.Series, np.ndarray]] = None,
        color: Optional[str] = None,
        related_hist_component: Optional[HistogramComponent] = None,
        line_style: str = "-",
    ) -> HistogramComponent:
        hist_data, hist_weights = self.prepare_data_and_weights(data=data, weights=weights)
        hist_component = HistogramComponent(
            data=hist_data,
            label=label,
            weights=hist_weights,
            color=color,
            related_component=related_hist_component,
            line_style=line_style,
        )
        self._histogram.add_signal_component(hist_component=hist_component)
        return hist_component

    def add_data(
        self,
        data: Union[pd.DataFrame, pd.Series, np.ndarray],
        label: str,
        color: Optional[str] = None,
    ) -> None:
        hist_data, hist_weights = self.prepare_data_and_weights(data=data)
        hist_component = HistogramComponent(
            data=hist_data,
            label=label,
            weights=hist_weights,
            color=color,
        )
        self._histogram.add_data(hist_component=hist_component)

    def get_binning(self) -> Union[int, np.ndarray]:
        return self.hist_var.bins

    def plot_on(
        self,
        legend_pos: Optional[str] = None,
        legend_title: Optional[str] = None,
        fig_ax: Tuple[FigureType, AxesType] = None,
        add_pull: bool = False,
        ncol: int = 1,
        factor: Optional[float] = None,
        show_legend: bool = True,
        custom_xticks=None,
        lumi_pos=None,
        legend_fontsize=16,
    ) -> Tuple[FigureType, AxesType]:
        set_matplotlibrc_params()

        if add_pull:
            fig, axes = plt.subplots(
                nrows=2,
                ncols=1,
                sharex=True,
                figsize=self.fig_size,
                gridspec_kw={"height_ratios": [13, 2], "hspace": 0.05},
                constrained_layout=True,
            )
            ax, ax2 = axes
        else:
            if fig_ax is None:
                fig, ax = plt.subplots(figsize=self.fig_size)
            else:
                fig, ax = fig_ax
            ax2 = None

        if self.hist_type == "stepfilled":
            kwargs = {"lw": 0.3, "edgecolor": "black"}
        else:
            kwargs = {"lw": 1.5}

        if self.histogram.components is not None:
            ax.hist(
                self.histogram.get_bins_for_hist(),
                bins=self._histogram.get_binning(),
                weights=self.histogram.get_bin_counts(),
                label=self.histogram.get_labels(),
                color=self.histogram.get_colors(),
                histtype=self.hist_type,
                stacked=self.stacked,
                density=self.normed,
                **kwargs,
            )

            if self.uncertainty:
                ax.bar(
                    self.histogram.get_bins_for_hist()[0],
                    height=2 * self.histogram.get_bin_errors(),
                    width=self.histogram.get_bin_width(),
                    bottom=self.histogram.get_total_bin_count() - self.histogram.get_bin_errors(),
                    color="black",
                    hatch="///////",
                    fill=False,
                    lw=0,
                    label="MC stat. unc.",
                )

            _, ymax = ax.get_ylim()

        if self.histogram.signal_components is not None:
            for signal_component in self.histogram.signal_components:
                signal_bin_count, _ = self.histogram.get_signal_bin_count_for_component(hist_component=signal_component)
                ax.hist(
                    self.histogram.get_signal_bins_for_hist()[0],
                    bins=self.histogram.get_binning(),
                    weights=signal_bin_count,
                    label=f"{signal_component.label}",
                    color=signal_component.color,
                    histtype="step",
                    lw=3,
                    ls=signal_component.line_style,
                )
                if self.uncertainty:
                    bin_errors = self.histogram.get_signal_bin_error_for_component(hist_component=signal_component)
                    ax.bar(
                        self.histogram.get_signal_bins_for_hist()[0],
                        height=2 * bin_errors,
                        width=self.histogram.get_bin_width(),
                        bottom=signal_bin_count - bin_errors,
                        edgecolor=signal_component.color,
                        hatch="///////",
                        fill=False,
                        lw=0,
                    )

        if self.histogram.data_components is not None:
            for data_component in self.histogram.data_components:
                bin_count = self.histogram.get_bin_count_for_component(hist_component=data_component)
                bin_count = [b if b > 0 else np.nan for b in bin_count]
                ax.errorbar(
                    self.histogram.get_data_bins_for_hist()[0],
                    bin_count,
                    yerr=np.sqrt(bin_count),
                    label=data_component.label,
                    color=data_component.color,
                    marker="o",
                    markersize=8,
                    capsize=4,
                    lw=3,
                    ls="None",
                )

        if add_pull:
            assert ax2 is not None
            assert self.histogram.data_components is not None
            ax2.fill_between(
                self.hist_var.scope, y1=(-1, -1), y2=(1, 1), color=KITColors.grey, alpha=0.5, edgecolor="None"
            )
            ax2.fill_between(
                self.hist_var.scope, y1=(-1, -1), y2=(-2, -2), color=KITColors.grey, alpha=0.25, edgecolor="None"
            )
            ax2.fill_between(
                self.hist_var.scope, y1=(1, 1), y2=(2, 2), color=KITColors.grey, alpha=0.25, edgecolor="None"
            )

            data_component = self.histogram.data_components[0]
            pull = (
                self.histogram.get_bin_count_for_component(hist_component=data_component)
                - self.histogram.get_total_bin_count()
            ) / (
                np.sqrt(
                    self.histogram.get_total_bin_count()
                    + self.histogram.get_bin_count_for_component(hist_component=data_component)
                )
            )
            ax2.errorbar(
                self.histogram.get_data_bins_for_hist()[0],
                pull,
                marker="o",
                ls="None",
                color=KITColors.kit_black,
                markersize=8,
            )
            ax2.set_ylim(-5, 5)
            ax2.axhline(0, color=KITColors.dark_grey)

            width = self.histogram.get_bin_width() / 15
            for i, value in enumerate(pull):
                if value > 5.1:
                    x = self.histogram.get_data_bins_for_hist()[0][i]
                    ax2.arrow(
                        x=x,
                        y=2,
                        dx=0,
                        dy=3,
                        length_includes_head=True,
                        width=width,
                        head_width=3 * width,
                        head_length=1.0,
                        color="black",
                    )
                    ax2.text(x, 1, round(value, 1), fontsize=8, color="black", ha="center", va="center")
                if value < -5.1:
                    x = self.histogram.get_data_bins_for_hist()[0][i]
                    ax2.arrow(
                        x=x,
                        y=-2,
                        dx=0,
                        dy=-3,
                        length_includes_head=True,
                        width=width,
                        head_width=3 * width,
                        head_length=1.0,
                        color="black",
                    )
                    ax2.text(x, -1, round(value, 1), fontsize=8, color="black", ha="center", va="center")

            ax2.set_ylabel(r"Pull")
            ax2.set_yticks([-3, 0, 3])
            if custom_xticks:
                ax2.set_xticks(custom_xticks)

        if self.hist_var.scope:
            ax.set_xlim(self.hist_var.scope)

        if self.y_log:
            ax.set_yscale("log")

        if self.luminosity_label:
            ymin, ymax = ax.get_ylim()
            if factor is None:
                factor = 1.1 if not self._additional_lumi_text else 1.2
            ax.set_ylim(ymin, factor * ymax)
            if not lumi_pos:
                ax.text(0.02, 0.96, self.luminosity_label, va="top", transform=ax.transAxes, fontsize=15)
            else:
                ax.text(
                    lumi_pos[0],
                    lumi_pos[1],
                    self.luminosity_label,
                    ha=lumi_pos[2],
                    va="top",
                    transform=ax.transAxes,
                    fontsize=15,
                )

        ax.set_ylabel(self.y_label, loc="top")

        if not add_pull:
            ax.set_xlabel(self.hist_var.x_label, loc="right")
        else:
            fig.align_ylabels([ax, ax2])
            ax2.set_xlabel(self.hist_var.x_label, loc="right")
        l_pos = "best" if not self.hist_var.x_scale_log else "upper left"
        if legend_pos:
            l_pos = legend_pos
        if show_legend:
            ax.legend(
                loc=l_pos,
                fontsize=legend_fontsize,
                title=legend_title,
                title_fontsize=legend_fontsize,
                ncol=ncol,
                mode="expand" if ncol > 1 else None,
            )

        if self.title:
            ax.set_title(
                self.title,
                loc="right",
                fontsize=14,
            )

        if add_pull:
            plt.subplots_adjust(hspace=0.05, wspace=0.02)

        return fig, ax

    @property
    def hist_var(self) -> HistVariable:
        return self._hist_var

    @property
    def title(self) -> Optional[str]:
        return self._title

    @property
    def stacked(self) -> bool:
        return self._stacked

    @property
    def hist_type(self) -> str:
        return self._hist_type

    @property
    def normed(self) -> bool:
        return self._normed

    @property
    def uncertainty(self) -> bool:
        return self._uncertainty

    @property
    def y_log(self) -> bool:
        return self._y_log

    @property
    def luminosity_label(self) -> Optional[str]:
        if not self.histogram.data_components:
            base_text = r"$\mathbf{Belle~II \, Simulation}$"
        else:
            base_text = r"$\mathbf{Belle~II}$"
        if not self._luminosity:
            if not self._additional_lumi_text:
                return base_text
            else:
                return base_text + f"\n{self._additional_lumi_text}"
        else:
            text_str = (
                base_text + " " + r"$\int \mathcal{L} \mathrm{d}t= $" + f"{self._luminosity}" + r" $\mathrm{fb}^{-1}$"
            )
            if not self._additional_lumi_text:
                return text_str
            else:
                return text_str + f"\n{self._additional_lumi_text}"

    @property
    def fig_size(self) -> Tuple[float, float]:
        return self._fig_size

    @property
    def histogram_plot_type(self) -> HistogramPlotType:
        return self._histogram_plot_type

    @property
    def y_label(self) -> str:
        if self.normed:
            y_label = f"{self.histogram_plot_type.value} in arb. units"
        else:
            y_label = "{e} / {bo}{b:.4g}{v}{bc}".format(
                e=self.histogram_plot_type.value,
                b=self.histogram.get_bin_width(),
                v=" " + self.hist_var.unit if self.hist_var.unit else "",
                bo="(" if self.hist_var.unit else "",
                bc=")" if self.hist_var.unit else "",
            )
        return y_label

    @property
    def histogram(self) -> Histogram:
        return self._histogram
