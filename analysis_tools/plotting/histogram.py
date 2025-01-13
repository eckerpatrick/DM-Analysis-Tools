from typing import List, Optional, Tuple

import numpy as np
import copy

from analysis_tools.plotting.plot_variables import HistVariable
from analysis_tools.plotting.histogram_component import HistogramComponent

__all__ = [
    "Histogram",
]


class Histogram:
    def __init__(self, variable: HistVariable) -> None:
        self._variable = variable

        self._components = None  # type: Optional[List[HistogramComponent]]
        self._signal_components = None  # type: Optional[List[HistogramComponent]]

        self._data_components = None  # type: Optional[List[HistogramComponent]]

    def add_component(self, hist_component: HistogramComponent) -> None:
        if self.components is None:
            self._components = []
        assert self._components is not None
        self._components.append(hist_component)

    def add_signal_component(self, hist_component: HistogramComponent) -> None:
        if self.signal_components is None:
            self._signal_components = []
        assert self._signal_components is not None
        self._signal_components.append(hist_component)

    def add_data(self, hist_component: HistogramComponent) -> None:
        if self.data_components is None:
            self._data_components = []
        assert self._data_components is not None
        self._data_components.append(hist_component)

    def get_binning(self) -> np.ndarray:
        if self.variable.scope:
            start, stop = self.variable.scope
        else:
            all_data = [comp.data for comp in self.all_components]
            start = np.min([np.min(x) for x in all_data])
            stop = np.max([np.max(x) for x in all_data])
        return np.linspace(start, stop, self.variable.bins + 1)

    def get_bin_width(self) -> float:
        binning = self.get_binning()
        assert len(binning) >= 2
        return binning[1] - binning[0]

    def get_bins_for_hist(self) -> List[np.ndarray]:
        binning = self.get_binning()
        bin_mids = [(binning[i] + binning[i + 1]) / 2 for i in range(0, len(binning) - 1)]
        assert self.components is not None
        return [np.array(bin_mids) for _ in self.components]

    def get_signal_bins_for_hist(self) -> List[np.ndarray]:
        binning = self.get_binning()
        bin_mids = [(binning[i] + binning[i + 1]) / 2 for i in range(0, len(binning) - 1)]
        assert self.signal_components is not None
        return [np.array(bin_mids) for _ in self.signal_components]

    def get_data_bins_for_hist(self) -> List[np.ndarray]:
        binning = self.get_binning()
        bin_mids = [(binning[i] + binning[i + 1]) / 2 for i in range(0, len(binning) - 1)]
        assert self.data_components is not None
        return [np.array(bin_mids) for _ in self.data_components]

    def get_bin_count_for_component(self, hist_component: HistogramComponent) -> np.ndarray:
        bin_count, _ = np.histogram(
            hist_component.data,
            bins=self.get_binning(),
            weights=hist_component.weights,
        )
        return bin_count

    def get_bin_counts(self) -> List[np.ndarray]:
        bin_counts = []  # type: List[np.ndarray]
        assert self.components is not None
        for component in self.components:
            bin_count = self.get_bin_count_for_component(hist_component=component)
            bin_counts.append(bin_count)
        return bin_counts

    def get_total_bin_count(self) -> np.ndarray:
        return np.sum(self.get_bin_counts(), axis=0)

    def get_bin_error_for_component(self, hist_component: HistogramComponent) -> np.ndarray:
        bin_errors_squared, _ = np.histogram(
            hist_component.data,
            bins=self.get_binning(),
            weights=hist_component.weights**2 if isinstance(hist_component.weights, np.ndarray) else None,
        )
        return np.sqrt(bin_errors_squared)

    def get_bin_errors(self) -> np.ndarray:
        assert self.components is not None
        return np.sqrt(
            np.sum(
                [self.get_bin_error_for_component(hist_component=component) ** 2 for component in self.components],
                axis=0,
            )
        )

    def get_signal_bin_count_for_component(self, hist_component: HistogramComponent) -> Tuple[np.ndarray, float]:
        bin_count = self.get_bin_count_for_component(hist_component=hist_component).astype(float)
        if not hist_component.related_component:
            if self.components is not None:
                max_bin_count = np.max(bin_count)
                if max_bin_count == 0:
                    return bin_count, 1.0
                max_bin_counts = np.max(np.sum(self.get_bin_counts(), axis=0))
                scaling = max_bin_counts / max_bin_count
            else:
                scaling = 1
            bin_count *= scaling
        else:
            _, scaling = self.get_signal_bin_count_for_component(hist_component=hist_component.related_component)
            bin_count *= scaling

        return bin_count, scaling

    def get_signal_bin_counts(self) -> List[np.ndarray]:
        signal_bin_counts = []  # type: List[np.ndarray]
        assert self.signal_components is not None
        for component in self.signal_components:
            bin_count, _ = self.get_signal_bin_count_for_component(hist_component=component)
            signal_bin_counts.append(bin_count)
        return signal_bin_counts

    def get_signal_bin_error_for_component(self, hist_component: HistogramComponent) -> np.ndarray:
        _, scaling = self.get_signal_bin_count_for_component(hist_component=hist_component)
        return scaling * self.get_bin_error_for_component(hist_component=hist_component)

    def get_colors(self) -> Optional[List[Optional[str]]]:
        assert self.components is not None
        colors = [comp.color for comp in self.components]
        if all(c is not None for c in colors):
            return colors
        else:
            return None

    def get_signal_colors(self) -> Optional[List[Optional[str]]]:
        assert self.signal_components is not None
        colors = [comp.color for comp in self.signal_components]
        if all(c is not None for c in colors):
            return colors
        else:
            return None

    def get_labels(self) -> List[str]:
        assert self.components is not None
        labels = [comp.label for comp in self.components]
        return labels

    def get_signal_labels(self) -> List[str]:
        assert self.signal_components is not None
        labels = [f"{comp.label} in a.u." for comp in self.signal_components]
        return labels

    @property
    def variable(self) -> HistVariable:
        return self._variable

    @property
    def components(self) -> Optional[List[HistogramComponent]]:
        return self._components

    @property
    def signal_components(self) -> Optional[List[HistogramComponent]]:
        return self._signal_components

    @property
    def data_components(self) -> Optional[List[HistogramComponent]]:
        return self._data_components

    @property
    def all_components(self):
        all_components = copy.copy(self.components)
        if self.signal_components is not None:
            all_components.extend(self.signal_components)
        if self.data_components is not None:
            all_components.extend(self.data_components)
        return all_components
